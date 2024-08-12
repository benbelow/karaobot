from data.models.word import Word
from data.repositories.wordRepository import WordRepository
from parody.analysis.WordAnalyser import analyse_word, analyse_sentence


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def import_words(lines):
    lines = [l for l in lines]
    if not lines:
        return

    repo = WordRepository()

    # this doesn't look super performant, at least once initial import is done.
    # would probably be better to just check for words that already exist upfront rather than loading everything into memory
    existing = [w.word for w in repo.fetch_all_words()]

    for line_batch in batch(lines, 1000):
        dtos = []
        for line in line_batch:
            sentence = analyse_sentence(line.strip())
            for analysed_word in sentence:
                if analysed_word.rawWord not in existing:
                    dto_word = Word(
                        word=analysed_word.rawWord,
                        stress=analysed_word.stress,
                        nltk_part_of_speech=analysed_word.nltkPartOfSpeech,
                        spacy_part_of_speech=analysed_word.spacy_pos,
                        spacy_morph=analysed_word.spacy_morph)
                    dtos.append(dto_word)
                    existing.append(dto_word.word)

        repo.bulk_insert_words(dtos)
        # print("Imported " + str(len(dtos)) + " words.")
        # print("Last Seen: " + line_batch[-1])
