#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the transcriber class and methods."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"
__date__ = "06/23"

# Built-in modules
import typing
import os
from abc import ABC, abstractmethod

# Third-party libraries
import torch
import whisper

# Local modules
from transcription import Transcription

# Global variables
DEFAULT_TEMPERATURE_TRANSCRIBER = 0.1
DEFAULT_MODEL_SIZE_TRANSCRIBER = "medium"


class AbstractTranscriber(ABC):
    """Abstract base class for an audio to text."""

    @abstractmethod
    def transcribe(self, filename: str) -> None:
        """Transcribe the audio from a file."""
        pass


class WhisperTranscriber(AbstractTranscriber):
    """Transcriber that uses whisper model."""

    def __init__(
        self,
        model_size: str = DEFAULT_MODEL_SIZE_TRANSCRIBER,
        temperature: float = DEFAULT_TEMPERATURE_TRANSCRIBER,
    ):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.temperature = temperature
        self.model = whisper.load_model(model_size, device=self.device)

    def transcribe(self, audio_filename: str) -> str:
        """Transcribe the audio from a file using whisper model."""

        # Check if file exists
        if not os.path.isfile(audio_filename):
            raise FileNotFoundError(f"Audio file {audio_filename} not found.")

        # Call whisper
        result = self.model.transcribe(
            audio_filename,
            verbose=False,
            fp16=False,
            task="transcribe",
            temperature=self.temperature,
        )

        # Retrieve transcription
        transcription = Transcription()
        transcription.set_language(result["language"])

        for segment in result["segments"]:
            transcription.add_transcription(
                start=segment["start"],
                end=segment["end"],
                text=segment["text"],
            )

        return transcription


if __name__ == "__main__":
    """Test the Transcriber."""
    transcriber = WhisperTranscriber(model_size="small", temperature=0.1)

    test_filename = "./../audios/foo.mp3"
    transcription = transcriber.transcribe(test_filename)

    print(f"Transcription language detected: {transcription.language}\n")

    print(f"Transcription: {transcription.get_text()}\n")

    time_to_look_up = 0.2
    print(
        f"Look up time {time_to_look_up} s: {transcription.look_up_time(time_to_look_up)}\n"
    )

    word_to_look_up = "Mauricio"
    print(
        f"Word {word_to_look_up}: was found between {transcription.look_up_word(word_to_look_up)} s"
    )

    pass
