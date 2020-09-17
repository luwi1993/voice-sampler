import pandas as pd
import os
import librosa
class TextParser:
    def __init__(self, mode=""):
        self.mode = mode
        self.inside_quotes = []
        self.durations = []
        self.name = []
        self.text = []
        self.prep_text = []

    def load_file(self, path="files/transcriptions/transcriptions.csv"):
        df = pd.read_csv(path, sep ="|")
        vals = df.values
        self.name = vals[:,0]
        self.text = vals[:,1]
        self.prep_text =vals[:,2]

    def get_duration(self, wav_dir="files/samples/"):
        self.durations = []
        for file_name in os.listdir(wav_dir):
            if file_name == "README.txt":
                continue
            samples, sample_rate = librosa.load(wav_dir+file_name)
            self.durations.append(librosa.get_duration(samples, sample_rate))


    def get_inside_quotes(self, wav_dir="files/samples/"):
        n_files = len(os.listdir(wav_dir))
        self.inside_quotes = [False for _ in range(n_files)]

    def parse_list(self):
        for char in self.file:
            if char in ["0","1"]:
                break

t = TextParser()
t.load_file()
t.get_duration()
t.get_inside_quotes()
print(t.inside_quotes)
print(t.durations)