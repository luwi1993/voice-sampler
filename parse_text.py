import os

import librosa
import numpy as np
import pandas as pd


class TextParser:
    def __init__(self, mode=""):
        self.mode = mode
        self.inside_quotes = []
        self.durations = []
        self.name = []
        self.text = []
        self.prep_text = []
        self.n_entrys = 0
        self.replacements = [("Mr.", "Mister"),
                             ("Mrs.", "Misess"),
                             ("Dr.", "Doctor"),
                             ("No.", "Number"),
                             ("St.", "Saint"),
                             ("Co.", "Company"),
                             ("Jr.", "Junior"),
                             ("Maj.", "Major"),
                             ("Gen.", "General"),
                             ("Drs.", "Doctors"),
                             ("Rev.", "Reverend"),
                             ("Lt.", "Lieutenant"),
                             ("Hon.", "Honorable"),
                             ("Sgt.", "Sergeant"),
                             ("Capt.", "Captain"),
                             ("Esq.", "Esquire"),
                             ("Ltd.", "Limited"),
                             ("Col.", "Colonel"),
                             ("Ft.", "Fort")]
        self.deletions = ['"',":",";",",",")","(","5","1","2","3","4","6","7","8","9","0"]

    def replace_abbreviation(self, word, abb, full):
        if word == abb:
            word = full
        return word

    def get_prep_text(self):
        prep_text = []
        for line in self.text:
            prep_line = ""
            for word in line.split(" "):
                for char in word:
                    prep_word = ""
                    if not char in self.deletions:
                        prep_word += char.lower()
                for abb, full in self.replacements:
                    prep_word = self.replace_abbreviation(prep_word, abb, full)
                prep_line += prep_word + " "
            prep_text.append(prep_line[:-1])
        self.prep_text = prep_text

    def load_file(self, path="files/transcriptions/transcriptions.csv"):
        df = pd.read_csv(path, sep="|")
        vals = df.values
        self.name = vals[:, 0]
        self.text = vals[:, 1]
        self.prep_text = vals[:, 2]
        self.n_entrys = len(df)

    def get_duration(self, wav_dir="files/samples/"):
        self.durations = []
        for file_name in os.listdir(wav_dir):
            if file_name == "README.txt":
                continue
            samples, sample_rate = librosa.load(wav_dir + file_name)
            self.durations.append(librosa.get_duration(samples, sample_rate))

    def get_inside_quotes(self, wav_dir="files/samples/"):
        n_files = len(os.listdir(wav_dir))
        self.inside_quotes = [False for _ in range(n_files)]

    def get_transctripts(self):
        transctripts = np.asarray([[a, b, c, d, e] for a, b, c, d, e in
                                   zip(self.name, self.text, self.prep_text, self.inside_quotes, self.durations)])
        df = pd.DataFrame(transctripts,
                          columns=["id", "transcription", "normalized_transcription", "is_inside_quote", "duration"],)
        return df

    def safe_transctripts(self, path="files/transcriptions/transcript.csv"):
        transctripts = self.get_transctripts()
        transctripts.to_csv(path, sep="|",index=False,header=False)

    def print(self):
        self.get_transctripts().head(10)

    def preprocess(self):
        self.load_file()
        self.get_duration()
        self.get_inside_quotes()
        self.get_prep_text()
        self.safe_transctripts()

TextParser().preprocess()