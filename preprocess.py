import matplotlib.pyplot as plt
import numpy as np
import librosa
from scipy.io.wavfile import write
from ui_tools import play

class VoicePreprocessor:
    def __init__(self, fs=22050):
        self.fs  = fs

    def load(self, path):
        self.samples, self.sample_rate = librosa.load(path)
        self.duration = librosa.get_duration(self.samples)
        self.n_samples = len(self.samples)

    def plot(self):
        plt.plot(np.arange(self.n_samples)/self.sample_rate ,self.samples)
        plt.show()

    def filter(self, threshold = 0.0005):
        above_threshold = threshold < np.abs(self.samples)
        self.samples = self.samples[above_threshold]
        self.n_samples = len(self.samples)

    def write(self, path):
        write(path, self.sample_rate, self.samples)

    def preprocess_voice(self, path):
        self.load(path)
        self.filter()
        self.write(path)
