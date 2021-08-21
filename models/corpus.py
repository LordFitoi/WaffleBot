from json import load
from os.path import abspath, dirname, join

class Corpus:
    root_dir = dirname(dirname(abspath(__file__))) 

    def __init__(self, name="es"):
        corpus_path = join(self.root_dir, f"corpus/{name}.json")
        
        with open(corpus_path, "r") as jsonfile:
            self.data = load(jsonfile)