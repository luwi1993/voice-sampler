import os

import librosa
import numpy as np
import pandas as pd
import ui_tools as ui

class TextParser:
    def __init__(self, mode=""):
        self.mode = mode
        self.all_inside_quotes = []
        self.all_durations = []
        self.all_filenames = []
        self.all_transcriptions = []
        self.all_prep_transcriptions = []
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

    def parse_transcription(self, transcription):
        prep_transcription = ""
        for word in transcription.split(" "):
            for abb, full in self.replacements:
                word = self.replace_abbreviation(word, abb, full)
            prep_word = ""
            for char in word:
                if not char in self.deletions:
                    prep_word += char.lower()

            prep_transcription += prep_word + " "
        return prep_transcription[:-1]

    def get_duration(self, path):
        samples, sample_rate = librosa.load(path)
        return librosa.get_duration(samples, sample_rate)

    def get_inside_quotes(self, transcription):
        return False


    def replace_abbreviation(self, word, abb, full):
        if word == abb:
            word = full
        return word

    def find_valid_transcription(self, path ="files/samples/"):
        valid = []
        for i,name in enumerate(self.all_filenames):
            if os.path.isfile(path+str(name)):
                valid.append(i)
        return valid

    def filter_valid_transcription(self):
        valids = self.find_valid_transcription()
        print(len(valids),"of",len(self.all_filenames),"transcriptions are valid")
        self.all_filenames = np.asarray(self.all_filenames)[valids].tolist()
        self.all_transcriptions = np.asarray(self.all_transcriptions)[valids].tolist()
        self.all_prep_transcriptions = np.asarray(self.all_prep_transcriptions)[valids].tolist()
        self.all_inside_quotes = np.asarray(self.all_inside_quotes)[valids].tolist()
        self.all_durations = np.asarray(self.all_durations)[valids].tolist()

    def edit_text(self, path="files/transcriptions/transcriptions.csv"):
        names = []
        for name in self.all_filenames:
            name=str(name)
            if name[:-4] != ".wav":
                name+=".wav"
            names.append(name)
        self.all_filenames = names



    def prep_all_transcriptions(self):
        prep_text = []
        for transcription in self.all_transcriptions:
            prep_text.append(self.parse_transcription(transcription))
        self.all_prep_transcriptions = prep_text

    def load_file(self, path="files/transcriptions/transcript.csv"):
        df = pd.read_csv(path, sep="|")
        vals = df.values
        self.all_filenames = vals[:, 0]
        self.all_transcriptions = vals[:, 1]
        self.n_entrys = len(df)



    def get_all_durations(self, wav_dir="files/samples/"):
        self.all_durations = []
        for file_name in os.listdir(wav_dir):
            if file_name == "README.txt":
                continue
            self.all_durations.append(self.get_duration(wav_dir + file_name))



    def get_all_inside_quotes(self, wav_dir="files/samples/"):
        n_files = len(os.listdir(wav_dir))
        self.all_inside_quotes = [self.get_inside_quotes("") for _ in range(n_files)]

    def get_transctripts_df(self):
        transctripts = np.asarray([[a, b, c, d, e] for a, b, c, d, e in
                                   zip(self.all_filenames, self.all_transcriptions, self.all_prep_transcriptions, self.all_inside_quotes, self.all_durations)])
        df = pd.DataFrame(transctripts,
                          columns=["id", "transcription", "normalized_transcription", "is_inside_quote", "duration"],)
        return df

    def safe_transctripts(self, path="files/transcriptions/transcript.csv"):
        transctripts = self.get_transctripts_df()
        transctripts.to_csv(path, sep="|",index=False,header=False)

    def print(self):
        self.get_transctripts_df().head(10)

    def cleanup_transcript(self, source="files/transcriptions/transcriptions.csv", file="files/transcriptions/transcript_clean.csv"):
        self.load_file(source)
        self.edit_text()
        self.get_all_durations()
        self.get_all_inside_quotes()
        self.prep_all_transcriptions()
        self.filter_valid_transcription()
        self.filter_valid_wav()
        self.safe_transctripts(file)

    def find_valid_wav(self, wav_dir="files/samples/"):
        valids = []
        invalids = []
        file_names = os.listdir(wav_dir)
        if self.all_filenames:
            for file in file_names:
                if not file in self.all_filenames:
                    invalids.append(file)
                else:
                    valids.append(file)
        return valids, invalids


    def filter_valid_wav(self,wav_dir="files/samples/"):
        valinds, invalids = self.find_valid_wav(wav_dir)
        print(len(valinds),"of",(len(valinds)+len(invalids)),"files are valid")
        print("invalids:",invalids)
        if ui.check_remove():
            for file in invalids:
                os.remove(wav_dir+file)


t= TextParser()
t.cleanup_transcript()
