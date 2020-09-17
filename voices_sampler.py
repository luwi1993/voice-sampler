import sounddevice as sd
from scipy.io.wavfile import write
import ui_tools as ui
import time
import numpy as np
import pandas as pd
import os
from preprocess import VoicePreprocessor

class VoiceSampler:
    def __init__(self, fs=22050, seconds=3, file_path="files/", go_signal_path="go.wav", device='digital output'):
        self.fs = fs
        self.seconds = seconds
        self.file_path = file_path
        self.go_signal_path = file_path + go_signal_path
        self.device = device
        self.transctripts = []
        self.voice_preprocessor = VoicePreprocessor()

    def go_signal(self):
        input("press enter when ready")
        ui.play(self.go_signal_path)

    def record(self, path):
        recording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=2)
        sd.wait()
        write(path, self.fs, recording)

    def make_transcript_entry(self, id=0, transcription="", normalized_transcription=""):
        self.transctripts.append([id, transcription, normalized_transcription])

    def save_transcript(self, path, sep ="|"):
        if self.transctripts:
            df = pd.DataFrame(np.asarray(self.transctripts), columns=["id", "transcription", "normalized_transcription"])
            if os.path.isfile(path):
                old_transcripts = pd.read_csv(path, sep=sep)
                df = old_transcripts.append(df)
            print(str(len(df))+" entrys saved total")
            df.to_csv(path, sep=sep, index=False)
            self.transctripts = []

    def sample(self, transcription=""):
        id = str(time.time())
        ui.show_transcription(transcription, self.go_signal)
        path = self.file_path + "samples/" + id + ".wav"
        self.record(path)
        self.voice_preprocessor.preprocess_voice(path)
        finished, success = ui.check_finished(path, transcription, self.sample)
        if success:
            self.make_transcript_entry(id=id, transcription=transcription, normalized_transcription=transcription)
    def sample_transcription(self, transcriptions_batch, max_len = 100):
        N = len(transcriptions_batch)
        transcription = transcriptions_batch[np.random.randint(0,N)]
        if len(transcription) > max_len:
            transcription = self.sample_transcription(transcriptions_batch)
        return transcription

    def make_dataset(self, transcriptions_batch, n_samples=10):
        transcript_path = self.file_path + "transcriptions/transcriptions.csv"
        for _ in range(n_samples):
            transcription = self.sample_transcription(transcriptions_batch)
            self.sample(transcription)
            self.save_transcript(transcript_path)

if __name__ == "__main__":
    transcription = pd.read_csv("files/metadata.csv", sep="|").values[:,1].tolist()[:10000]
    v = VoiceSampler(seconds=10)
    v.make_dataset(transcription)
