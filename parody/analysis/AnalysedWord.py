import prosodic as prosodic


class AnalysedWord:
    def __init__(self, raw_word):
        self.rawWord = raw_word
        self.prosodicWord = prosodic.Word(raw_word)

    def stress(self):
        return self.prosodicWord.stress
