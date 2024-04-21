#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the Meeting class and methods."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"

# Built-in modules
import os
import typing

# Third-party libraries
from datetime import date

# Local modules
from . import recorders
from . import transcribers
from . import summarizers
from . import bots

# Global variables
from .gpt_wrapper import DEFAULT_GPT_MODEL
from .recorders import DEFAULT_AUDIO_FORMAT
from .transcribers import (
    DEFAULT_TEMPERATURE_TRANSCRIBER,
    DEFAULT_MODEL_SIZE_TRANSCRIBER,
)
from .summarizers import DEFAULT_TEMPERATURE_SUMMARIZER
from .bots import DEFAULT_BOT_TEMPERATURE


class Meeting:
    """Class representing a meeting."""

    def __init__(
        self,
        audio_filename: str = None,
        participant_names: list[str] = None,
        dt: date = None,
        whisper_model_size: str = DEFAULT_MODEL_SIZE_TRANSCRIBER,
        temperature_transcription: float = DEFAULT_TEMPERATURE_TRANSCRIBER,
        temperature_summarizer=DEFAULT_TEMPERATURE_SUMMARIZER,
        gpt_model: str = DEFAULT_GPT_MODEL,
    ):
        self.audio_filename = audio_filename

        self.participant_names = participant_names or [""]
        self.date = dt or date.today()

        self.transcriber = transcribers.WhisperTranscriber(
            model_size=whisper_model_size, temperature=temperature_transcription
        )

        self.summarizer = summarizers.GPTSummarizer(
            model=gpt_model, temperature=temperature_summarizer
        )

    def record(
        self, audio_filename: str, audio_format: str = DEFAULT_AUDIO_FORMAT
    ) -> None:
        """Record the meeting audio."""
        recorder = recorders.FfmpgRecorder()
        recorder.record(audio_filename, audio_format)
        self.audio_filename = audio_filename + "." + audio_format

    def transcribe(self) -> str:
        """Get the transcription of the meeting."""
        if not os.path.isfile(self.audio_filename):
            raise FileNotFoundError(f"Audio file {self.audio_filename} not found.")

        self.transcription = self.transcriber.transcribe(self.audio_filename)
        self.audio_language = self.transcription.language
        self.transcription_text = self.transcription.get_text()

        return self.transcription.get_text()

    def _has_a_transcription(self) -> bool:
        """Check if the meeting has a transcription."""
        return hasattr(self, "transcription")

    def summarize(self, language: str = None) -> str:
        """Get a summary of the meeting."""

        if not self._has_a_transcription():
            self.transcribe()

        language = self.transcription.language if language is None else language
        text_summary = self.summarizer.summarize(self.transcription_text, language)
        self.summary = text_summary
        return self.summary

    def keywords(self) -> str:
        if not self._has_a_transcription():
            self.transcribe()

        keywords = self.answer(
            "Extract a list of 6 keywords with the most important information from the meeting."
            + "Answer only the with a list of keywords separated by a comma."
        )

        self.keywords = keywords
        return self.keywords

    def answer(
        self,
        question: str,
        gpt_model=DEFAULT_GPT_MODEL,
        bot_temperature=DEFAULT_BOT_TEMPERATURE,
    ) -> str:
        """Get an answer to the question regarding the meeting."""
        if not hasattr(self, "transcription"):
            self.transcribe()

        self.bot = bots.GPTQABot(gpt_model=gpt_model, temperature=bot_temperature)

        return self.bot.answer(question, self.transcription_text)

    def look_up_word(self, word: str) -> typing.List[tuple[float, float]]:
        """Look up the start and end times of a specific word in the transcription."""
        if not self._has_a_transcription():
            self.transcribe()

        return self.transcription.look_up_word(word)

    def look_up_time(self, time: float) -> str:
        """Look up the words spoken at a specific time in the transcription."""
        if not self._has_a_transcription():
            self.transcribe()

        return self.transcription.look_up_time(time)
