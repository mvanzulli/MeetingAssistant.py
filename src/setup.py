from setuptools import setup, find_packages

setup(
    name="meeting_assistant",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "torch",
        "openai-whisper",
        "ffmpeg",
        "tiktoken",
        "pyyaml",
        "numpy",
        "datetime",
        "langdetect",
        "googletrans==4.0.0-rc1",
        "setuptools",
        "pytest",
    ],
    author="Mauricio Vanzulli",
    author_email="mcvanzulli@gmail.com",
    description="A package to interact with meetings",
    keywords="openai, whisper, torch, meetings, speech recognition, summarization",
)
