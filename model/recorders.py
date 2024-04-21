#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Module defining the recorder tools ."""

__author__ = "Mauricio Vanzulli"
__email__ = "mcvanzulli@gmail.com"
__date__ = "02/22"

# Built-in modules
import time
import sys
import subprocess
import threading
import signal
import os
from abc import ABC, abstractmethod

# Third-party libraries
import ffmpeg

# Constant variables
DEFAULT_AUDIO_FORMAT = "mp3"


class AbstractRecorder(ABC):
    """Abstract base class for a recorder."""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def record(self, *args, **kwargs):
        pass

    def display_clock(self) -> None:
        start_time = time.time()
        while not self.stop_timer:
            elapsed_time = time.time() - start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            sys.stdout.write(f"\rRecording: {minutes:02d}:{seconds:02d}")
            sys.stdout.flush()
            time.sleep(1)


class FfmpgRecorder(AbstractRecorder):
    """Recorder that uses FFmpeg."""

    def __init__(self):
        super().__init__()
        self.acodec = "alsa" if sys.platform == "linux" else "avfoundation"

    def record(
        self, output_filename: str, output_format: str = DEFAULT_AUDIO_FORMAT
    ) -> None:
        self.stop_timer = False

        # Add the extension to the output filename
        output_filename = f"{output_filename}.{output_format}"
        try:
            # Start the moving timer in a different thread
            timer_thread = threading.Thread(target=self.display_clock)
            timer_thread.start()

            stream = (
                ffmpeg.input("default", f=self.acodec, ac=2, video_size=None)
                .output(
                    output_filename, acodec="libmp3lame", format=output_format
                )  # Specify the output format as 'mp3'
                .overwrite_output()
            )

            # Start the process
            process = ffmpeg.run_async(stream, pipe_stdin=True, pipe_stderr=True)

            # Wait for the process to finish or be interrupted
            while process.poll() is None:
                time.sleep(1)

        except KeyboardInterrupt:
            self.stop_timer = True
            timer_thread.join()

            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process.wait()

            print(f"\n Recording has been saved in: {output_filename}")

        except Exception as e:
            print(e)
            raise


if __name__ == "__main__":
    FfmpgRecorder().record(output_filename="test", output_format="mp3")
