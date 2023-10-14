import prosodic as prosodic
import nltk as nltk
import spacy
nlp = spacy.load("en_core_web_sm")

nlp.tokenizer.rules = {key: value for key, value in nlp.tokenizer.rules.items() if
                       "'" not in key and "’" not in key and "‘" not in key}

def analyse_sentence(raw_sentence):
    raw_sentence = raw_sentence.lower()
    sentence = nlp(raw_sentence)
    return [analyse_word(sw.text, sw) for sw in sentence]


def analyse_word(raw_word, spacy_word=None):
    """
    Three types of analysis currently in place:
    * Prosodic = covers scansion / amphasis
    * nltk = one option for nlp.
    * spacy = an alternate option for nlp. Works between with context, so optional spacy_word param can be used to
    pass pre-analysed words from a sentence
    """
    prosodic_word = prosodic.Word(raw_word)
    stress = prosodic_word.stress

    if raw_word != "":
        tokenized = nltk.word_tokenize(raw_word)
        part_of_speech = nltk.pos_tag(tokenized)[0][1]

        if spacy_word is None:
            spacy_word = nlp(raw_word)[0]

        spacy_pos = spacy_word.pos_
        spacy_morph = spacy_word.morph.__str__()
    else:
        part_of_speech = None
        spacy_pos = None
        spacy_morph = None

    return AnalysedWord(raw_word, stress, part_of_speech, spacy_pos, spacy_morph)


# TODO: Should we just use the database DTO in a small project?
class AnalysedWord:
    def __init__(self, raw_word, stress, nltk_part_of_speech, spacy_pos, spacy_morph):
        self.rawWord = raw_word
        self.stress = stress
        self.nltkPartOfSpeech = nltk_part_of_speech
        self.spacy_pos = spacy_pos
        self.spacy_morph = spacy_morph


def get_pos(word):
    tokenized = nltk.word_tokenize(word)
    return nltk.pos_tag(tokenized)[0][1]