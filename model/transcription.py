#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the transcription class and methods."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"
__date__ = "06/23"

from abc import ABC, abstractmethod

# Built-in modules
import typing


class AbstractTranscription(ABC):
    """Abstract base class for a transcription."""

    @abstractmethod
    def add_transcription(self, start: float, end: float, text: str) -> None:
        """Add a transcription."""
        pass

    @abstractmethod
    def set_language(self, language: str) -> None:
        """Set the language of the transcription."""
        pass

    @abstractmethod
    def get_text(self) -> str:
        """Get the text of the transcription."""
        pass

    @abstractmethod
    def look_up_time(self, time: float) -> str:
        """Look up the transcription at a specific time."""
        pass

    @abstractmethod
    def look_up_word(self, word: str) -> typing.List[tuple[float, float]]:
        """Look up the start and end times of a specific word in the transcription."""
        pass


class Transcription:
    """Class to store the audio transcription."""

    def __init__(self, language: str = None):
        self.transcriptions = []
        self.language = language

    def add_transcription(self, start: float, end: float, text: str) -> None:
        self.transcriptions.append({"start": start, "end": end, "text": text})

    def set_language(self, language: str) -> None:
        self.language = language

    def get_text(self) -> str:
        text = ""
        for transcription in self.transcriptions:
            text += transcription["text"] + " "
        return text

    def look_up_time(self, time: float) -> str:
        for transcription in self.transcriptions:
            if transcription["start"] <= time and transcription["end"] >= time:
                return transcription["text"]
        return ""

    def look_up_word(self, word: str) -> typing.List[tuple[float, float]]:
        times = []
        for transcription in self.transcriptions:
            if word in transcription["text"]:
                times.append((transcription["start"], transcription["end"]))
        return times
