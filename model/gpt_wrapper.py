#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the Meeting class and methods."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"
__date__ = "06/23"

# Built-in modules
import os

# Third-party libraries
import openai

DEFAULT_GPT_MODEL = "gpt-3.5-turbo"
DEFAULT_GPT_ENCODER = "cl100k_base"
DEFAULT_MAX_TOKENS = 2000


def call_gpt(
    encoded_prompt: str,
    command_prompt: str,
    role: str,
    temperature: float,
    model: str = DEFAULT_GPT_MODEL,
) -> str:
    """
    Generate a summary prompt using OpenAI's GPT language model.
    """

    # Get command role and prompts from the config file
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": f"{role}"},
            {"role": "user", "content": f"{command_prompt}: {encoded_prompt}"},
        ],
        temperature=temperature,
    )
    return response.choices[0].message["content"].strip()
