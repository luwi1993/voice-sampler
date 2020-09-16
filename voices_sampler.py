import sounddevice as sd
from scipy.io.wavfile import write
import ui_tools as ui
import time
import numpy as np
import pandas as pd


class VoiceSampler:
    def __init__(self, fs=44100, seconds=3, file_path="files/", go_signal_path="go.wav", device='digital output'):
        self.fs = fs
        self.seconds = seconds
        self.file_path = file_path
        self.go_signal_path = file_path + go_signal_path
        self.device = device
        self.transctripts = []

    def go_signal(self):
        input("press enter when ready")
        ui.play(self.go_signal_path)

    def record(self, path):
        recording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=2)
        sd.wait()
        write(path, self.fs, recording)

    def make_transcript_entry(self, id=0, transcription="", normalized_transcription=""):
        self.transctripts.append([id, transcription, normalized_transcription])

    def save_tramscript(self, path):
        df = pd.DataFrame(np.asarray(self.transctripts), columns=["id", "transcription", "normalized_transcription"])
        df.to_csv(path, sep="|")

    def sample(self, transcription=""):
        id = str(time.time())
        ui.show_transcription(transcription, self.go_signal)
        path = self.file_path + "samples/" + id + ".wav"
        self.record(path)
        finished, success = ui.check_finished(path, transcription, self.sample)
        if success:
            self.make_transcript_entry(id=id, transcription=transcription, normalized_transcription=transcription)

    def make_dataset(self, transcriptions):
        try:
            id = str(time.time())
            for transcription in transcriptions:
                self.sample(transcription)
            self.save_tramscript(self.file_path + "transcriptions/transcriptions_" + id + ".csv")
        except:
            self.save_tramscript(self.file_path + "transcriptions/transcriptions_" + id + ".csv")

transcription = pd.read_csv("files/metadata.csv", sep="|").values[:,1].tolist()[:10]
v = VoiceSampler(seconds=3)
v.make_dataset(transcription)
