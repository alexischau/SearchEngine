import json

class Posting:
    def __init__(self, n, freq):
        self.docid = n

        # calculate (1 + log(freq))
        self.tfidf = freq
    
    def encode(self):
        return self.__dict__
