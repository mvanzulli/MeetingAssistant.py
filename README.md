# 🎙️ Meeting Assistant

This program provides functionality to record meetings and then generate summaries of the transcribed audio using OpenAI's GPT-3 language model.

<img src="https://github.com/mvanzulli/Meeting_Assistant/assets/50339940/a42a1587-8084-4a57-a10a-470365c60a87" alt="ui_picture" width="800" height="400">

## 🚀 Prerequisites

To run this program, you will need:

- `Python 3.7` or higher
- `ffmpeg` installed on your system. If not:
  ```bash
  sudo apt install ffmpeg
  ```

## 🔧 Installation


  1. Clone this repository
  2. Create an enviroment and install dependencies
  ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
  ```

## 🔑 Required Environment Variables

This program requires an OpenAI API key to function. To set up your environment variables:

1. Create a new file named `.env` in the root of this directory
2. Add the following line to your `.env` file: `OPEN_API_KEY=<your_api_key>`
3. Replace `<your_api_key>` with your actual OpenAI API key.

## 🛠️ Usage

### UI 

Launch the Web-UI: 
  
```bash
./run.sh
```

Launch the GUI: 
  
```bash
python3 gui/gui.py
```

### Record

To record a meeting, run:

```bash
python model/model.py record <output_file_name>.mp3
```

This will record the audio and save it to a file with the specified name.

### Summarize

To generate a summary of an audio file, run:

```bash
python3 model/model.py summarize <audio_file_name>.mp3 
```

This will generate a summary of the transcribed audio using OpenAI's GPT-3 language model in the same audio language.

### Translate and Summarize

To generate a summary of an audio file and translate it into <language_key>, run:

```bash
python3 model/model.py summarize <audio_file_name>.mp3 <language_key>
```
You can see the language keys in the language_roles.yaml file.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💼 Variables to tune

<details>
<summary> Feel free to change: </summary>
 
This program has several variables that can be tuned to change its behavior. These variables are declared at the beginning of the program:

- `OS`: Set this to `"linux"` or `"MAC"` depending on your operating system.
- `DEVICE`: Set this to `"cuda:0"` if you have an NVIDIA GPU and want to use it to accelerate processing, or `"cpu"` to use the CPU instead.
- `WHISPER_MODEL`: The name of the pre-trained Whisper model to use for transcribing the audio.
- `ENV_OPENAI_KEY`: The name of the environment variable that contains your OpenAI API key.
- `TEMPERATURE`: The "temperature" parameter to use when generating summaries with GPT-3. Higher values will generate more diverse summaries, while lower values will generate more conservative summaries.
- `GPT_MODEL`: The name of the GPT-3 language model to use for generating summaries.
- `GPT_ENCODER`: The name of the GPT-3 tokenizer to use for encoding text.
- `SIZE_CHUNK`: The size of each "chunk" of text to send to GPT-3 for summarization. Larger chunks will result in fewer requests to the API, but may be slower to process.
- Command prompts and command role in the `language_roles.yaml` file.
