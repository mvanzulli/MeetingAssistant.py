from meeting_assistant.bots import GPTQABot
from meeting_assistant.bots import bot_roles, DEFAULT_BOT_TEMPERATURE
from langdetect import detect


def test_bot_initialization():
    bot = GPTQABot("es")  # Use Spanish language
    assert bot.user_role == bot_roles["es"]["command_prompt"]
    assert bot.bot_role == bot_roles["es"]["command_role"]
    assert bot.temperature == DEFAULT_BOT_TEMPERATURE


def test_bot_answer():
    bot = GPTQABot()
    context = """
    In a meeting, the team discussed improving the performance of their software. They agreed on conducting a
    thorough performance assessment of their code the coming week.
    """
    question = "En que se pusieron de acuerdo?"
    answer = bot.answer(question, context)

    assert detect(answer) == "es"
