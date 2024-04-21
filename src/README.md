# 🎙️ Meeting Assistant 

This program provides functionality to record meetings and then generate summaries of the transcribed audio using OpenAI's GPT-3 language model. 

## Quick Start
```python
import os 

# Set your API key
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

from meeting_assistant import Meeting

# 📁 Load your meeting file 
m = Meeting("audio_file.mp3")

# 🎙️ Record a meeting and save it as an audio file.
m = Meeting().record("audio_file.mp3")

# 📝 Transcribe the audio file.
transcription = m.transcribe()

# 📋 Generate summary.
summary = m.summarize("en")

# ❓Answer a question about the meeting.
answer = m.answer("What are the next steps?")

# 🔍 Look up a specific word.
word_times = m.look_up_word("important")

# ⏰ Look up a specific time.
time_words = m.look_up_time(10.0)

# 🗝️ Get the keywords from your meeting.
keywords = m.keywords()
```
