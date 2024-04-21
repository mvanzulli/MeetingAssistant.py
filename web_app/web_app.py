#!/usr/bin/env python
import streamlit as st
import requests
import os
from typing import Tuple
from st_custom_components import st_audiorec

languages = ["es", "en", "fr", "pt", "de"]


def process_summary(summary: str) -> str:
    """
    Process the summary to make it more readable.

    Args:
        summary (str): The summary to
    """
    summary = summary[9:-1]

    return summary


# Function to call the API and get the summary
def summarize_audio(file, language: str, ip: str) -> Tuple[str, str, str]:
    url = f"{ip}/translate_summarize_audio/?language={language}"
    files = {"file": file}
    response = requests.post(url, files=files).json()
    summary = process_summary(response["summary"])
    transcription = response["transcription"]
    audio_language = response["audio_language"]
    return summary, transcription, audio_language


def main(BASE_URL: str):
    st.set_page_config(
        page_title="Meeting Assistant",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .centered-title {
            text-align: center;
            margin-top: -60px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h1 class="centered-title" style="color: red;">Meeting Assistant </h1>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 3])  # Divide the screen into two columns

    with col1:
        st.markdown("## :round_pushpin: Meeting Audio")

        with st.expander("Record a meeting and download audio file"):
            wav_audio_data = st_audiorec()
            if wav_audio_data is not None:
                # display audio data as received on the backend
                st.audio(wav_audio_data, format="audio/wav")

        with st.expander("Upload a meeting"):
            audio_file = st.file_uploader("Upload .mp3 audio file", type=["wav", "mp3"])

    with col2:
        if audio_file is not None:
            st.markdown("## :round_pushpin: Meeting Summary")
            language = st.selectbox("Select summary language", languages)
            if st.button("Generate Summary"):
                with st.spinner("Generating Summary..."):
                    summary, transcription, _ = summarize_audio(
                        audio_file, language, BASE_URL
                    )

                with st.expander("Summary and future work"):
                    st.write(summary)

                with st.expander("Transcription"):
                    st.write(transcription)


def is_running_in_docker():
    return os.path.exists("/.dockerenv")


if __name__ == "__main__":
    PORT = 8000
    BASE_URL = (
        f"http://model:{PORT}" if is_running_in_docker() else f"http://0.0.0.0:{PORT}"
    )

    main(BASE_URL)
