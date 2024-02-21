import pandas as pd

def singleton(cls):

    instance = [None]
    
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    
    return wrapper

@singleton
class Corpus:

    def __init__(self):
        self.corpus = []

    def load(self):
        # file = './data/' + FILE_PREFIX + '3' + ".json"
        data = pd.read_json("./data/dblp-ref-3.json", lines=True)
        self.corpus.append(data)
        self.corpus = pd.concat(self.corpus, ignore_index=True)

    def get(self):
        return self.corpus