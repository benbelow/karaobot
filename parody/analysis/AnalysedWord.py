import prosodic as prosodic
import nltk as nltk

class AnalysedWord:
    def __init__(self, raw_word):
        self.rawWord = raw_word
        self.prosodicWord = prosodic.Word(raw_word)

        if raw_word != "":
            tokenized = nltk.word_tokenize(raw_word)
            self.partOfSpeech = nltk.pos_tag(tokenized)[0][1]
        else:
            self.partOfSpeech = None

    def stress(self):
        return self.prosodicWord.stress
