import os

import librosa
import numpy as np
import pandas as pd


class TextParser:
    def __init__(self, mode=""):
        self.mode = mode
        self.inside_quotes = []
        self.durations = []
        self.names = []
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
        self.deletions = ['"',":",";",",",")","(","5","1","2","3","4","6","7","8","9","0","-",""]

    def replace_abbreviation(self, word, abb, full):
        if word == abb:
            word = full
        return word

    def find_valid(self, path = "files/samples/"):
        valid = []
        for i,name in enumerate(self.names):
            if os.path.isfile(path+name):
                valid.append(i)
        return valid

    def filter_valid(self):
        valids = self.find_valid()
        self.names = np.asarray(self.names)[valids].tolist()
        self.text = np.asarray(self.text)[valids].tolist()
        self.prep_text = np.asarray(self.prep_text)[valids].tolist()
        self.inside_quotes = np.asarray(self.inside_quotes)[valids].tolist()
        self.durations = np.asarray(self.durations)[valids].tolist()

    def edit_text(self, path="files/transcriptions/transcriptions.csv"):
        names = []
        for name in self.names:
            name=str(name)
            if name[:-4] != ".wav":
                name+=".wav"
            names.append(name)
        self.names = names

    def get_prep_text(self):
        prep_text = []
        for line in self.text:
            prep_line = ""
            for word in line.split(" "):
                for abb, full in self.replacements:
                    word = self.replace_abbreviation(word, abb, full)
                prep_word = ""
                for char in word:
                    if not char in self.deletions:
                        prep_word += char.lower()

                prep_line += prep_word + " "
            prep_text.append(prep_line[:-1])
        self.prep_text = prep_text

    def load_file(self, path="files/transcriptions/transcriptions.csv"):
        df = pd.read_csv(path, sep="|")
        vals = df.values
        self.names = vals[:, 0]
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
                                   zip(self.names, self.text, self.prep_text, self.inside_quotes, self.durations)])
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
        self.edit_text()
        self.get_duration()
        self.get_inside_quotes()
        self.get_prep_text()
        self.filter_valid()
        self.safe_transctripts()

TextParser().preprocess()