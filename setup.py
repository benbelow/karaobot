from data.models.word import Word
from data.repositories.wordRepository import WordRepository
from parody.analysis.AnalysedWord import analyse_word

with open("data/source_data/english_words_58_000.txt", 'r') as stop_words_file:
    lines = stop_words_file.readlines()

    dtos = []

    i = 0
    for line in lines:
        i += 1
        if i % 1000 == 0:
            print("Imported: " + str(i) + " words - last seen: " + line)
        word = analyse_word(line.strip())
        dtoWord = Word(word=word.rawWord, stress=word.stress, part_of_speech=word.partOfSpeech)
        dtos.append(dtoWord)

    repo = WordRepository()
    repo.bulk_insert_words(dtos)



