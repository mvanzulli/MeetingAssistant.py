#!/usr/bin/env python

# Libraries
import os
import sys
import time
import threading
import signal
import subprocess
import yaml
import ffmpeg
import openai
import tiktoken
import torch
import whisper
from dotenv import load_dotenv

# Set up environment variables
OS = "linux"
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Whisper
WHISPER_MODEL = "medium"

# Set the environment variable OPEN_API_KEY to your OpenAI API key
ENV_OPENAI_KEY = "OPEN_API_KEY"

# GPT 3.5 Turbo
TEMPERATURE = 0.7
GPT_MODEL = "gpt-3.5-turbo"
GPT_ENCODER = "cl100k_base"
SIZE_CHUNK = 2000
with open("language_roles.yaml", "r") as f:
    language_roles = yaml.safe_load(f)

# Init clock
stop_timer = False

def record_meeting(output_filename):
    """
    Record a meeting using ffmpeg and display a ticker on the console.

    This function records the audio and saves it to a file specified by output_filename.
    It also displays a timmer on the console showing the elapsed time since the recording started.
    The clock updates every second until the recording is stopped by the user or an error occurs.
    This function uses two threads to accomplish this.

    Args:
        output_filename (str): The name of the output file, including the file extension.

    Returns:
        None
    """
    try:
        global stop_timer

        # Start the moving timmer in a different thread
        stop_timer = False
        timer_thread = threading.Thread(target=display_clock)
        timer_thread.start()

        # Record the audio using ffmpeg
        output_format = "mp3"

        if OS == "linux":
            stream = (
                ffmpeg.input("default", f="alsa", ac=2, video_size=None)
                .output(
                    output_filename, acodec="libmp3lame", format=output_format
                )  # Specify the output format as 'mp3'
                .overwrite_output()
            )
        elif OS == "MAC":
            stream = (
                ffmpeg.input(":0", f="avfoundation", video_size=None)  # Use 'default'
                .output(
                    output_filename, acodec="libmp3lame", format=output_format
                )  # Specify the output format as 'mp3'
                .overwrite_output()
            )

        # Start the process
        process = ffmpeg.run_async(stream, pipe_stdin=True, pipe_stderr=True)

        # Wait for the process to finish or be interrupted
        while process.poll() is None:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_timer = True
        timer_thread.join()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait()

        print(f"\n Recording has been saved in: {output_filename} ")
    except Exception as e:
        print(e)


def display_clock():
    """
    Displays a clock on the console showing the elapsed time since the function was called.
    The ticker updates every second until the global variable stop_timer is set to True.

    Args: None

    Returns: None
    """
    start_time = time.time()
    while not stop_timer:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        sys.stdout.write(f"\rRecording: {minutes:02d}:{seconds:02d}")
        sys.stdout.flush()
        time.sleep(1)


def transcribe_audio(filename):
    """Transcribe the audio from a file using a pre-trained whisper model.

    This function loads a pre-trained whisper model, loads the audio from a file specified by filename,
    and transcribes the audio using the model. The function then returns the transcribed text.

    Args:
        filename (str): The name of the audio file to transcribe.

    Returns:
        str: The transcribed text as a string.
    """
    # load model
    model = whisper.load_model(WHISPER_MODEL, device=DEVICE)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(filename)

    print("Starting Transcribing Process With Automatic Language Detection...")

    result = model.transcribe(audio, verbose=False, fp16=False, task="transcribe")

    return result["text"], result["language"]


def summarize_and_translate(transcript, language="en"):
    """
    Generate a summary of a transcript using OpenAI's GPT-3 language model.

    This function takes in a transcript (a string) and generates a summary of the text using OpenAI's GPT-3 language model.
    The transcript is broken up into smaller chunks of text to improve performance with the GPT-3 API.
    The summary is returned as a string.

    Args:
        transcript (str): The transcript to summarize.
        language (str): The language of the transcript. Defaults to English.

    Returns:
        A string containing the summary of the transcript.
    """

    def generate_summary(prompt, language):
        """
        Generate a summary prompt using OpenAI's GPT-3 language model.

        This function takes in a prompt (a string) and generates a summary of the text using OpenAI's GPT-3 language model.
        The summary is returned as a string.

        Args:
            prompt (str): The prompt to summarize.
            language (str): The language of the prompt. Defaults to English.
        Returns:
            A string containing the summary of the prompt.
        """

        # Get the role and prompts fot the language
        role = language_roles[language]["command_role"]
        command_prompt = language_roles[language]["command_prompt"]

        # Get command role and prompts from the config file
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": f"{role}"},
                {"role": "user", "content": f"{command_prompt}: {prompt}"},
            ],
            temperature=TEMPERATURE,
        )
        return response.choices[0].message["content"].strip()

    # Initialize a list to store the smaller chunks of text
    chunks = []

    # Encode the text into tokens using the GPT-3 tokenizer
    tokenizer = tiktoken.get_encoding(GPT_ENCODER)
    tokens = tokenizer.encode(transcript)

    # Split the tokens into smaller chunks to better fit the GPT-3 API's request size limit
    while tokens:
        chunk_tokens = tokens[:SIZE_CHUNK]
        # Convert the chunk back into text
        chunk_text = tokenizer.decode(chunk_tokens)
        # Add the chunk to the list of chunks
        chunks.append(chunk_text)
        # Move on to the next set of tokens
        tokens = tokens[SIZE_CHUNK:]

    summary = "\n".join([generate_summary(chunk, language) for chunk in chunks])

    return summary


def print_output(transcript, summary, language):
    """
    Print the transcript and summary to the console.

    This function takes in a transcript (a string) and a summary (a string) and prints them to the console.

    Args:
        transcript (str): The transcript to print.
        summary (str): The summary to print.
        language (str): The language of the transcript. Defaults to English.
    Returns:
        None
    """
    print(f"TRANSCRIPTION OUTPUT START\n{transcript}\nTRANSCRIPTION OUTPUT END\n")
    print(f"SUMMARY LANGUAGE:\n{language}\n")
    print(
        f"SUMMARY AND FUTURE WORK OUTPUTS START\n{summary}\nSUMMARY AND FUTURE WORK OUTPUTS END\n"
    )

    return None


if __name__ == "__main__":
    # Get the OpenAI API key from the environment
    load_dotenv()
    api_key = os.getenv(ENV_OPENAI_KEY)

    if api_key is None:
        print(
            f"Please set an environment variable: {ENV_OPENAI_KEY} points to the OpenIA API key. Exiting..."
        )
        sys.exit(1)
    openai.api_key = api_key

    # Check input dimensions
    assert (
        len(sys.argv) >= 2
    ), "Usage: python3 record|summarize <output_file_name>.mp3 <language (optional)>"

    # Get actions and output filename from the command line
    action = sys.argv[1]
    output_filename = sys.argv[2]

    # Record action
    if action == "record":
        assert len(sys.argv) == 3, "Usage: python3 record <output_file_name>.mp3"
        record_meeting(output_filename)

    elif action == "summarize":
        assert (
            len(sys.argv) == 3 or len(sys.argv) == 4
        ), "Usage: python3 summarize <output_file_name>.mp3 <language (optional)>"

        if len(sys.argv) == 3:
            print(
                "No language specified. Using default language detected in the record"
            )

            transcript, language = transcribe_audio(output_filename)
            summary = summarize_and_translate(transcript, language)

            print_output(transcript, summary, language)
            sys.exit(1)
        else:
            language = sys.argv[3]
            # Check language is in the keys of the language_roles dictionary
            assert (
                language in language_roles.keys()
            ), f"Language {language} not supported. Please use one of the following languages explicit: {language_roles.keys()}"
            transcript, _ = transcribe_audio(output_filename)
            summary = summarize_and_translate(transcript, language)

            print_output(transcript, summary, language)
            sys.exit(1)
    else:
        print(
            f"Action {action} not supported. Please use one of the following actions: record, summarize"
        )
        sys.exit(1)
