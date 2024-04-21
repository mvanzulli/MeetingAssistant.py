#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the Meeting class and methods."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"
__date__ = "06/23"

# Built-in modules
import os

# Local modules
import recorders
import transcribers
import summarizers
import bots

# Global variables
from gpt_wrapper import DEFAULT_GPT_MODEL
from recorders import DEFAULT_AUDIO_FORMAT
from transcribers import DEFAULT_TEMPERATURE_TRANSCRIBER, DEFAULT_MODEL_SIZE_TRANSCRIBER
from summarizers import DEFAULT_TEMPERATURE_SUMMARIZER
from bots import DEFAULT_BOT_TEMPERATURE


class Meeting:
    """Class representing a meeting."""

    def __init__(
        self,
        audio_filename: str = None,
        whisper_model_size: str = DEFAULT_MODEL_SIZE_TRANSCRIBER,
        temperature_transcription: float = DEFAULT_TEMPERATURE_TRANSCRIBER,
        temperature_summarizer=DEFAULT_TEMPERATURE_SUMMARIZER,
        bot_temperature: float = DEFAULT_BOT_TEMPERATURE,
        gpt_model: str = DEFAULT_GPT_MODEL,
    ):
        self.audio_filename = audio_filename

        self.transcriber = transcribers.WhisperTranscriber(
            model_size=whisper_model_size, temperature=temperature_transcription
        )

        self.summarizer = summarizers.GPTSummarizer(
            model=gpt_model, temperature=temperature_summarizer
        )

        self.bot = bots.GPTQABot(temperature=bot_temperature)

    def record(self, audio_filename: int, audio_format=DEFAULT_AUDIO_FORMAT) -> None:
        """Record the meeting audio."""
        recorder = recorders.FfmpgRecorder()
        recorder.record(audio_filename, audio_format)
        self.audio_filename = audio_filename

    def transcribe(self) -> str:
        """Get the transcription of the meeting."""
        if not os.path.isfile(self.audio_filename):
            raise FileNotFoundError(f"Audio file {self.audio_filename} not found.")

        self.transcription = self.transcriber.transcribe(self.audio_filename)
        self.audio_language = self.transcription.language
        self.transcription_text = self.transcription.get_text()

        return self.transcription.get_text()

    def summarize(self, language: str = None) -> str:
        """Get a summary of the meeting."""

        if not hasattr(self, "transcription"):
            self.transcribe()

        language = self.transcription.language if language is None else language

        text_summary = self.summarizer.summarize(self.transcription_text, language)

        self.summary = text_summary

        return self.summary

    def answer(self, question: str) -> str:
        """Get an answer to the question regarding the meeting."""
        if not hasattr(self, "transcription"):
            self.transcribe()

        return self.bot.answer(question, self.transcription_text)


if __name__ == "__main__":
    """Test the Meeting."""
    meeting = Meeting("./../audios/foo.mp3")

    print("Transcription:")
    print(meeting.transcribe())

    print("\nSummary:")
    print(meeting.summarize("en"))

    print("\nAnswer:")
    print(meeting.answer("What is the next step?"))
