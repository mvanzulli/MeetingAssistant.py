import pytest
from meeting_assistant.transcribers import WhisperTranscriber
from meeting_assistant.transcriptions import Transcription


@pytest.fixture()
def transcriber():
    return WhisperTranscriber(model_size="tiny", temperature=0.1)


def test_whisper_transcriber(transcriber: WhisperTranscriber):
    """Test the Transcriber."""

    test_filename = "./../audios/foo.mp3"
    transcriptions = transcriber.transcribe(test_filename)

    assert isinstance(transcriptions, Transcription), "Transcriptions should be a list"
    assert transcriptions.language == "es", "Language should be Spanish"
    assert isinstance(
        transcriptions.get_text(), str
    ), "Transcription should not be None"

    time_to_look_up = 0.2
    time_found = transcriptions.look_up_time(time_to_look_up)
    assert isinstance(time_found, str), f"Look up time {time_to_look_up} s"

    word_to_look_up = "Mauricio"
    word_found = transcriptions.look_up_word(word_to_look_up)
    assert isinstance(word_found, list), f"Word {word_to_look_up}"
