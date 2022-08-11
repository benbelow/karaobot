import prosodic as prosodic
import nltk as nltk


def analyse_word(raw_word):
    prosodic_word = prosodic.Word(raw_word)
    stress = prosodic_word.stress

    if raw_word != "":
        tokenized = nltk.word_tokenize(raw_word)
        part_of_speech = nltk.pos_tag(tokenized)[0][1]
    else:
        part_of_speech = None

    return AnalysedWord(raw_word, stress, part_of_speech)


# TODO: Should we just use the database DTO in a small project?
class AnalysedWord:
    def __init__(self, raw_word, stress, part_of_speech):
        self.rawWord = raw_word
        self.stress = stress
        self.partOfSpeech = part_of_speech

    def stress(self):
        return self.stress
