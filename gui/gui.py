#!/usr/bin/env python

import sys
import os
import signal
import yaml
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QTextEdit,
    QHBoxLayout,
    QComboBox,
)
from PyQt5.QtCore import QProcess

# Read language options
with open("./../model/language_roles.yaml", "r") as f:
    language_roles = yaml.safe_load(f)
languages = list(language_roles.keys())

MEETING_ASSISTANT_CLI = "./../model/model.py"


class MeetingAssistant(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QR process and layout
        self.setWindowTitle("Meeting Assistant")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.button_layout = QHBoxLayout()
        layout.addLayout(self.button_layout)

        # Process
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        self.process.waitForFinished(-1)

        # Record start
        self.start_button = QPushButton("Record")
        self.start_button.clicked.connect(self.start_recording)
        self.button_layout.addWidget(self.start_button)

        # Record stop
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_recording)
        self.button_layout.addWidget(self.stop_button)

        # Summarize
        self.summarize_button = QPushButton("Summarize")
        self.summarize_button.clicked.connect(self.summarize)
        layout.addWidget(self.summarize_button)

        # Language selection
        self.language_label = QLabel("Select language:")
        layout.addWidget(self.language_label)
        self.language_combo = QComboBox()
        self.language_combo.addItems(languages)
        layout.addWidget(self.language_combo)

        # Transcript
        self.transcript_label = QLabel("Audio transcription:")
        layout.addWidget(self.transcript_label)
        self.transcript_edit = QTextEdit()
        layout.addWidget(self.transcript_edit)

        # Summary
        self.summary_label = QLabel("Audio summary and future works:")
        layout.addWidget(self.summary_label)
        self.summary_edit = QTextEdit()
        layout.addWidget(self.summary_edit)

    def start_recording(self):
        output_filename, _ = QFileDialog.getSaveFileName(
            self, "Save Meeting Recording", filter="MP3 Files (*.mp3)"
        )
        if not output_filename:
            return
        if not output_filename.endswith(".mp3"):
            output_filename += ".mp3"
        self.output_filename = output_filename
        self.process.start(
            "python", [MEETING_ASSISTANT_CLI, "record", self.output_filename]
        )

    def stop_recording(self):
        os.kill(self.process.processId(), signal.SIGINT)

    def process_finished(self):
        print("Process finished")

    def summarize(self):
        audio_filename, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", filter="MP3 Files (*.mp3)"
        )
        if not audio_filename:
            return

        language = self.language_combo.currentText()

        self.process.start(
            "python", [MEETING_ASSISTANT_CLI, "summarize", audio_filename, language]
        )

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        print(f"stdout: {data.strip()}")  # Print stderr to console

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        lines = data.strip().splitlines()

        transcript = self.transcript_edit.toPlainText()
        summary = ""
        summary_flag = False

        for line in lines:
            print(line)

            if line.startswith("TRANSCRIPTION OUTPUT START"):
                summary = ""
            elif line.startswith("TRANSCRIPTION OUTPUT END"):
                self.transcript_edit.setPlainText(transcript.strip())
            elif line.startswith("SUMMARY AND FUTURE WORK OUTPUTS START"):
                summary_flag = True
            elif summary_flag:
                if line.startswith("SUMMARY AND FUTURE WORK OUTPUTS END"):
                    summary_flag = False
                else:
                    summary += line.strip() + "\n"
            else:
                transcript += line.strip() + "\n"

        self.summary_edit.setPlainText(summary.strip())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeetingAssistant()
    window.show()
    sys.exit(app.exec_())
