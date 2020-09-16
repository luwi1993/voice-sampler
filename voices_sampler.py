import librosa

import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
import time
import os
import numpy as np
import pandas as pd

class VoiceSampler:
    def __init__(self, fs=44100, seconds=3, file_path="files/", go_signal_path="go.wav", device='digital output'):
        self.fs = fs
        self.seconds = seconds
        self.file_path = file_path
        self.go_signal_path = file_path+go_signal_path
        self.device = device
        self.transcriptions = []

    def go_signal(self):
        self.play(self.go_signal_path)

    def play(self, path):
        data, fs = sf.read(path)
        sd.play(data, fs)
        status = sd.wait()
        return status

    def check_successful(self, path):
        _input = input("ok? [y/n] p for replay").lower()

        success = True
        if _input == "n":
            success = False
        elif _input == "p":
            self.play(path)
            self.check_successful(path)
        elif _input != "y":
            print("invalid entry")
            success = self.check_successful(path)
        return success

    def check_repeat(self, transcription):
        _input = input("repeat? [y/n]").lower()
        if _input == "y":
            repeat = True
        elif _input == "n":
            repeat = False
        else:
            print("invalid entry")
            self.check_repeat(transcription)
        return repeat

    def check_finished(self, path, transcription):
        self.play(path)
        success = self.check_successful(path)
        finished = True
        if not success:
            os.remove(path)
            repeat = self.check_repeat(transcription)
            if repeat:
                finished = self.sample(transcription)
            else:
                finished = True
        return finished, success

    def record(self, path):
        recording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=2)
        sd.wait()
        write(path, self.fs, recording)

    def show_transcription(self, transcription):
        print(transcription)
        time.sleep(1)
        self.go_signal()

    def make_transcript_entry(self, id=0, transcription="", normalized_transcription=""):
        self.transcriptions.append([id,transcription,normalized_transcription])

    def save_tramscript(self, path):
        df = pd.DataFrame(np.asarray(self.transcriptions),columns=["id","transcription","normalized_transcription"])
        df.to_csv(path, sep="\t")

    def sample(self, transcription="halllo ich bin lukas"):
        id = str(time.time())
        self.show_transcription(transcription)
        path = self.file_path + id + ".wav"
        self.record(path)
        finished, success = self.check_finished(path, transcription)
        if success:
            self.make_transcript_entry(id=id, transcription=transcription, normalized_transcription=transcription)

    def make_dataset(self, target_transcriptions):
        for transcription in target_transcriptions:
            self.sample(transcription)
        self.save_tramscript(self.file_path+"transcriptions.csv")

transcription = ["A","B", "C"]
v = VoiceSampler(seconds=1)
v.make_dataset(transcription)
