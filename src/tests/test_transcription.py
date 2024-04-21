import pytest
from meeting_assistant.transcriptions import Transcription


def test_add_transcription():
    t = Transcription()
    t.add_transcription(0.0, 1.0, "Hello")
    assert len(t.transcriptions) == 1


def test_set_and_get_language():
    t = Transcription()
    t.set_language("en")
    assert t.language == "en"


def test_get_text():
    t = Transcription()
    t.add_transcription(0.0, 1.0, "Hello")
    t.add_transcription(1.0, 2.0, "there")
    assert t.get_text() == "Hello there "


def test_look_up_time():
    t = Transcription()
    t.add_transcription(0.0, 1.0, "Hello")
    t.add_transcription(1.0, 2.0, "there")
    assert t.look_up_time(1.5) == "there"
    assert t.look_up_time(0.5) == "Hello"


def test_look_up_word():
    t = Transcription()
    t.add_transcription(0.0, 1.0, "Hello")
    t.add_transcription(1.0, 2.0, "there")
    assert t.look_up_word("Hello") == [(0.0, 1.0)]
