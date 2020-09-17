

class TextParser:
    def __init__(self, mode=""):
        self.mode = mode

    def load_file(self, path):
        with open(path,mode="r") as file:
            self.file = file.read()

    def parse_list(self):
        for char in self.file:
            if char in ["0","1"]:
                break

t = TextParser()
t.load_file("files/harvard_sentences.txt")
print(t.file[:10])