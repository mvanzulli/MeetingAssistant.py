import os
import inspect
from meeting_assistant import Meeting

file_path = inspect.getframeinfo(inspect.currentframe()).filename
file_dir = os.path.dirname(os.path.abspath(file_path))

test_audio_filename = os.path.join(file_dir, "foo.mp3")

# 📁 Load your meeting file.
m = Meeting(
    test_audio_filename,
    participant_names=["Mauricio"],
    whisper_model_size="small",
    temperature_summarizer=0.5,
    gpt_model="gpt-4",  # gpt-3.5-turbo
)

# 📝 Transcribe your meeting.
transcription = m.transcribe()

# Look up a word in your meeting.
word_to_look_up = "mauricio"
word_times = m.look_up_word(word_to_look_up)
num_times = len(word_times)
print(
    f"Looked up `{word_to_look_up}`: It was mentioned between {word_times[0][0]} s and {word_times[0][1]} s."
)

# 📋 Summarize your meeting.
language = "en"
summary = m.summarize(language=language)
print("Summary:", summary)

# 🤖 Ask a question about your meeting.
next_steps = m.answer("What is the next step?")
print("Next steps:", next_steps)

# ❓ Get the keywords from your meeting.
keywords = m.keywords()
print("Keywords:", keywords)
