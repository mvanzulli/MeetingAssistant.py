import pytest
from meeting_assistant import Meeting

test_filename = "./../audios/foo.mp3"

m = Meeting(test_filename, whisper_model_size="tiny")


@pytest.fixture()
def meet():
    return Meeting(
        test_filename,
        whisper_model_size="tiny",
        participant_names=["Mauricio", "Robert"],
    )


def test_transcribe(meet: Meeting):
    transcription = meet.transcribe()
    assert type(transcription) is not None, "Transcription should not be None"


def test_summarize(meet: Meeting):
    summary = meet.summarize("en")
    assert isinstance(summary, str) is not None, "Summary should not be None"


def test_answer(meet: Meeting):
    answer = meet.answer("What is the next step?")
    assert isinstance(answer, str), "Answer should not be None"


def test_has_a_transcription(meet: Meeting):
    meet.transcribe()  # make sure a transcription occurs for this test
    assert meet._has_a_transcription() == True, "Transcription should exist."


def test_look_up_word(meet: Meeting):
    word_times = meet.look_up_word("mauricio")
    assert isinstance(word_times, list), "look_up_word should return a list"


def test_look_up_time(meet: Meeting):
    time_words = meet.look_up_time(0.1)
    assert isinstance(time_words, str), "look_up_time should return a string."
