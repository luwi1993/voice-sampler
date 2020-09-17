import matplotlib.pyplot as plt
import numpy as np
import librosa
from scipy.io.wavfile import write
from ui_tools import play


class VoicePreprocessor:
    def __init__(self, fs=22050):
        self.fs = fs

    def load(self, path):
        self.samples, self.sample_rate = librosa.load(path)
        self.duration = librosa.get_duration(self.samples)
        self.n_samples = len(self.samples)

    def plot(self):
        plt.plot(np.arange(self.n_samples) / self.sample_rate, self.samples)
        plt.show()

    def single_filter(self, threshold=0.0005):
        return threshold < np.abs(self.samples)

    def conv_filter(self, threshold=0.0005, window_size=100):
        c = np.convolve(np.abs(self.samples), [1/window_size for _ in range(window_size)], 'same')
        return threshold < c

    def get_filter(self, mode="single", threshold=0.001):
        if mode == "single":
            filter = self.single_filter(threshold)
        elif mode == "conv":
            filter = self.conv_filter(threshold)
        return filter

    def filter(self, mode="conv"):
        self.samples = self.samples[self.get_filter(mode=mode)]
        self.n_samples = len(self.samples)

    def write(self, path):
        write(path, self.sample_rate, self.samples)

    def preprocess_voice(self, path):
        self.load(path)
        self.filter()
        self.write(path)
