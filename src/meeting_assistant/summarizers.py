#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the summarizer class and methods."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"

# Built-in modules
from abc import ABC, abstractmethod

# Third-party libraries
import tiktoken
import yaml
import os
from pkg_resources import resource_string

# Local modules
from . import gpt_wrapper

# Global variables
from .gpt_wrapper import DEFAULT_GPT_MODEL, DEFAULT_GPT_ENCODER, DEFAULT_MAX_TOKENS

DEFAULT_TEMPERATURE_SUMMARIZER = 0.75

# Read the language roles from the config file
json_data = resource_string(__name__, "config/summarizer_roles.yaml")
summarizer_roles = yaml.safe_load(json_data)


class AbstractSummarizer(ABC):
    """Abstract base class for a text summarizer."""

    @abstractmethod
    def summarize(self, text: str) -> None:
        """Generate a summary of the given text."""
        pass


class GPTSummarizer(AbstractSummarizer):
    """Summarizer that uses OpenAI's GPT model."""

    def __init__(
        self,
        model: str = DEFAULT_GPT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE_SUMMARIZER,
        encoder: str = DEFAULT_GPT_ENCODER,
        max_tokes: float = DEFAULT_MAX_TOKENS,
    ):
        self.temperature = temperature
        self.model = model
        self.encoder = encoder
        self.max_tokens = max_tokes

    def summarize(self, text: str, language: str) -> str:
        """Generate a summary of the given text using GPT model."""

        # Encode the text into tokens using the GPT-3 tokenizer
        tokenizer = tiktoken.get_encoding(self.encoder)
        tokens = tokenizer.encode(text)

        # Split the tokens into smaller chunks to better fit the GPT-3 API's request size limit
        chunks = []
        while tokens:
            chunk_tokens = tokens[: self.max_tokens]
            # Convert the chunk back into text
            chunk_text = tokenizer.decode(chunk_tokens)
            # Add the chunk to the list of chunks
            chunks.append(chunk_text)
            # Move on to the next set of tokens
            tokens = tokens[self.max_tokens :]

        # Call OpenAI's GPT for each chunk and concatenate the results
        summary_text = ""
        for chunk in chunks:
            summary_text += gpt_wrapper.call_gpt(
                encoded_prompt=chunk,
                command_prompt=summarizer_roles[language]["command_prompt"],
                role=summarizer_roles[language]["command_role"],
                model=self.model,
                temperature=self.temperature,
            )

        return summary_text


if __name__ == "__main__":
    """Test the GPTSummarizer."""
    summarizer = GPTSummarizer(gpt_model="gpt-3.5-turbo", temperature=0.75)

    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, 
    unlike the natural intelligence displayed by humans and animals, 
    which involves consciousness and emotionality. The distinction between 
    the former and the latter categories is often revealed by the acronym 
    chosen. 'Strong' AI is usually labelled as AGI (Artificial General Intelligence) 
    while attempts to emulate 'natural' intelligence have been called ABI (Artificial 
    Biological Intelligence). Leading AI textbooks define the field as the study of 
    "intelligent agents": any device that perceives its environment and takes actions 
    that maximize its chance of successfully achieving its goals.
    """

    summary = summarizer.summarize(test_text, language="en")

    print(f"Summary: {summary}\n")
