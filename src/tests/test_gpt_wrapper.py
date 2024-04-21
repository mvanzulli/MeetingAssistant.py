from meeting_assistant.gpt_wrapper import call_gpt
import os


def test_api_key_set():
    assert "OPENAI_API_KEY" in os.environ


def test_call_gpt():
    encoded_prompt = "Hello"
    command_prompt = "Generate a response"
    role = "assistant"
    temperature = 0.7

    response = call_gpt(encoded_prompt, command_prompt, role, temperature)

    assert response.strip() != ""
