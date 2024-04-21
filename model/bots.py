#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the Meeting class and methods."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"
__date__ = "06/23"

# Built-in modules
from abc import ABC, abstractmethod

# Third-party libraries
import yaml

# Local modules
from gpt_wrapper import call_gpt

# Global variables
DEFAULT_BOT_TEMPERATURE = 0.5

# Read the language roles from the config file
with open("bot_roles.yaml", "r") as f:
    bots_roles = yaml.safe_load(f)


class AbstractQABot(ABC):
    """Abstract base class for a question and answer bot."""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass


class GPTQABot:
    def __init__(
        self, language: str = "en", temperature: float = DEFAULT_BOT_TEMPERATURE
    ) -> None:
        self.user_role = bots_roles[language]["command_prompt"]
        self.bot_role = bots_roles[language]["command_role"]
        self.temperature = temperature

    def answer(
        self, question: str, context: str, temperature: float = DEFAULT_BOT_TEMPERATURE
    ) -> str:
        return call_gpt(context, question, self.bot_role, temperature)


if __name__ == "__main__":
    qa_bot = GPTQABot()

    context = """
    In this text, Mauricio discusses how to develop a frontend. He explains the process of converting a function 
    or model into an endpoint to be containerized and served using FastAPI. He mentions that future work will 
    involve further development of the model, testing with FastAPI, and completing the interface.
    """

    question = "Which is the next step"

    answer = qa_bot.answer(question, context)

    print(answer)
