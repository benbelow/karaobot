from data.models.word import Word
from data.repositories.wordRepository import WordRepository
from parody.analysis.AnalysedWord import analyse_word


def import_words(raw_words):
    raw_words = [w for w in raw_words]
    if not raw_words:
        return
    dtos = []
    i = 0
    for raw_word in raw_words:
        i += 1
        if i % 1000 == 0:
            print("Imported: " + str(i) + " words - last seen: " + raw_word)
        word = analyse_word(raw_word.strip())
        dto_word = Word(word=word.rawWord, stress=word.stress, part_of_speech=word.partOfSpeech)
        dtos.append(dto_word)
    repo = WordRepository()
    repo.bulk_insert_words(dtos)
    print("Imported " + str(len(dtos)) + " words.")
