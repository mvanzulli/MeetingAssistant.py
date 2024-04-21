#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the Meeting class and methods."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"

# Built-in modules
from abc import ABC, abstractmethod

# Third-party libraries
import yaml
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from googletrans import Translator
from pkg_resources import resource_string

# Local modules
from . import gpt_wrapper

# Import global variables
from .gpt_wrapper import DEFAULT_GPT_MODEL

# Global variables
DEFAULT_BOT_TEMPERATURE = 0.5
DEFAULT_LANGUAGE = "en"

# Read the language roles from the config file
json_data = resource_string(__name__, "config/bot_roles.yaml")
bot_roles = yaml.safe_load(json_data)


class AbstractQABot(ABC):
    """Abstract base class for a question and answer bot."""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass


class GPTQABot:
    def __init__(
        self,
        language: str = "en",
        temperature: float = DEFAULT_BOT_TEMPERATURE,
        gpt_model: str = DEFAULT_GPT_MODEL,
    ) -> None:
        self.user_role = bot_roles[language]["command_prompt"]
        self.bot_role = bot_roles[language]["command_role"]
        self.temperature = temperature
        self.model = gpt_model

    def answer(
        self,
        question: str,
        context: str,
        temperature: float = DEFAULT_BOT_TEMPERATURE,
    ) -> str:
        # Detect language of the question
        try:
            question_language = detect(question)
            context_language = detect(context)
        except LangDetectException:
            question_language = DEFAULT_LANGUAGE

        if context_language != question_language:
            self.translator = Translator()
            context = self.translator.translate(context, dest=question_language).text

        # Set the bot_role to the detected language
        if question_language in bot_roles:
            self.bot_role = bot_roles[question_language]["command_role"]
            self.user_role = bot_roles[question_language]["command_prompt"]
        else:
            self.bot_role = bot_roles[DEFAULT_LANGUAGE][
                "command_role"
            ]  # Default to English
            self.user_role = bot_roles[DEFAULT_LANGUAGE]["command_prompt"]

        return gpt_wrapper.call_gpt(
            context, question, self.bot_role, temperature, self.model
        )
