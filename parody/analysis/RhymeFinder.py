from pyrhyme import rhyming_list

from data.models.word import WordRhyme
from data.repositories.RhymeRepository import RhymeRepository
from data.repositories.wordRepository import WordRepository
from parody.analysis.WordImporter import import_words
from stopwatch import Stopwatch

word_repo = WordRepository()
rhyme_repo = RhymeRepository()


def import_rhymes(db_word):
    sw = Stopwatch().start()
    raw_rhymes = rhyming_list(db_word.word, lang="en")
    raw_rhyme_words = [r.word for r in raw_rhymes]

    sw.split("RHYME, lookup")

    existing_words = [w.word for w in word_repo.get_words(raw_rhyme_words)]
    new_words = list(set(raw_rhyme_words) - set(existing_words))
    import_words(new_words)

    sw.split("RHYME, import results")


    # TODO: Store metadata on words e.g. offensiveness, frequency
    rhymes = [WordRhyme(word1=db_word.word, word2=r.word, score=r.score) for r in raw_rhymes]
    rhyme_repo.bulk_insert_rhymes(rhymes)

    sw.split("RHYME, insert rhymes")
