#!/usr/bin/env python
import time
import requests
import subprocess
from api import BASE_URL

# Run a python command from the root directory of the project
process = subprocess.Popen(['python', 'api.py'])

def translate_summarize_audio(
    file_to_summarize, language, method_to_test="translate_summarize_audio"
):
    url = f"{BASE_URL}/{method_to_test}/?language={language}"
    files = {"file": file_to_summarize}
    response = requests.post(url, files=files)
    return response.json()

def summarize_and_translate_text(
        text, language, method_to_test="translate_summarize_text"
    ):
        url = f"{BASE_URL}/{method_to_test}/?text={text}&language={language}"
        response = requests.get(url)
        return response.json()

def transcribe_audio(file_to_transcribe, method_to_test="transcribe"):
    url = f"{BASE_URL}/{method_to_test}/"
    response = requests.post(url, files={"file": file_to_transcribe})
    return response.json()

# Wait until the server is running
max_retries = 10  # Maximum number of retries
retry_delay = 2   # Delay between each retry
server_running = False
retries = 0

file_to_test = open("./audios/foo.mp3", "rb")
audio_language = "es"
summary_language = "en"
while not server_running and retries < max_retries:
    try:

        audio_summary = translate_summarize_audio(file_to_test, summary_language)
        assert type(audio_summary["summary"]) == str
        assert type(audio_summary["transcription"]) == str
        assert audio_summary["audio_language"] == "es"

        text = "Hey there, I am a test text. There is no future work, this is just a test"
        language = "en"
        summarize_output = summarize_and_translate_text(text, language)
        assert type(summarize_output["text"]) == str

        # TODO: Fix this test
        # transcribe_output = transcribe_audio(file_to_test)
        # assert type(transcribe_output["text"]) == str
        # assert transcribe_output["language"] == "es"

        server_running = True
    except:
        pass

    retries += 1
    time.sleep(retry_delay)
