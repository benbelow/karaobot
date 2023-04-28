from data.models.word import Word
from data.repositories.wordRepository import WordRepository
from parody.analysis.AnalysedWord import analyse_word


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def import_words(raw_words):
    raw_words = [w for w in raw_words]
    if not raw_words:
        return

    repo = WordRepository()

    for b in batch(raw_words, 1000):
        dtos = []
        for raw_word in b:
            word = analyse_word(raw_word.strip())
            dto_word = Word(
                word=word.rawWord,
                stress=word.stress,
                nltk_part_of_speech=word.nltkPartOfSpeech,
                spacy_part_of_speech=word.spacy_pos,
                spacy_morph=word.spacy_morph)
            dtos.append(dto_word)
        repo.bulk_insert_words(dtos)
        print("Imported " + str(len(dtos)) + " words.")
        print("Last Seen: " + b[-1])
