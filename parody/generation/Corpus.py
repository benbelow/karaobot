import random

from data.repositories.wordRepository import WordRepository
from parody.analysis.AnalysedWord import AnalysedWord, analyse_word
from pyrhyme import rhyming_list

from parody.analysis.RhymeFinder import import_rhymes

repo = WordRepository()


class WordGenOptions:
    def __init__(self, original, target_stress=None, rhyme_with=None, target_pos=None):
        self.original = original
        self.target_stress = target_stress

        # ORM WORD (not raw word) for use of join table
        self.rhyme_with = rhyme_with
        self.target_pos = target_pos


class Corpus:
    words_by_stress_then_speech_part = {}
    stop_words = []

    def __init__(self):
        words = repo.fetch_all_words()

        for db_word in words:
            word = AnalysedWord(raw_word=db_word.word, stress=db_word.stress, part_of_speech=db_word.part_of_speech)
            stress = word.stress
            pos = word.partOfSpeech

            if stress not in self.words_by_stress_then_speech_part:
                self.words_by_stress_then_speech_part[stress] = {}
            if pos not in self.words_by_stress_then_speech_part[stress]:
                self.words_by_stress_then_speech_part[stress][pos] = []

            self.words_by_stress_then_speech_part[stress][pos].append(word)

        with open("data/source_data/stop_words.txt", 'r') as stop_words_file:
            lines = stop_words_file.readlines()

            for line in lines:
                self.stop_words.append(line.strip())

    def get_word(self, generation_options):
        rhyme_with = generation_options.rhyme_with
        target_stress = generation_options.target_stress
        target_pos = generation_options.target_pos

        if len(target_stress) == 0:
            return analyse_word("")
        # TODO: Do we really need to analyse all stop words?
        if generation_options.original in self.stop_words:
            return analyse_word(generation_options.original)
        if rhyme_with is not None:
            return self.get_rhyming_word(rhyme_with, target_stress, target_pos)
        if target_stress is not None:
            return self.get_stressed_word(target_stress, target_pos)

    def get_rhyming_word(self, rhyme_with, target_stress, target_pos):
        if not rhyme_with.get_rhymes():
            rhyme_with = import_rhymes(rhyme_with)
            rhyme_with = repo.get_word(rhyme_with.word, load_rhymes=True)

        perfect_rhymes = [r for r in rhyme_with.get_rhymes() if r.score >= 300]
        imperfect_rhymes = [r for r in rhyme_with.get_rhymes() if r.score < 300]


        # TODO: Weight towards more common words for rhymes
        rhyme_source = perfect_rhymes if perfect_rhymes else imperfect_rhymes
        orm_rhymes = repo.get_words([r.word2 for r in rhyme_source])
        # TODO: Sort out mixture of AnalysedWord and DTO

        # TODO: Implement fallback for stress? Eg. PP might be a good replacement for UP if it rhymes, but is currently rejected
        valid_rhyming_words = [r.analysedWord() for r in orm_rhymes if r.stress == target_stress] \
            if target_stress is not None \
            else orm_rhymes

        # Needed for case where there *are* perfect rhymes, but none of them scan - so we want to check imperfect
        # rhymes that scan before giving up on rhyming
        if not valid_rhyming_words and perfect_rhymes:
            # TODO: Deduplicate this code
            rhyme_source = imperfect_rhymes
            orm_rhymes = repo.get_words([r.word2 for r in rhyme_source])
            valid_rhyming_words = [r.analysedWord() for r in orm_rhymes if r.stress == target_stress] \
                if target_stress is not None \
                else orm_rhymes

        return random.choice(valid_rhyming_words) \
            if len(valid_rhyming_words) != 0 \
            else self.get_stressed_word(target_stress, target_pos)

    def get_stressed_word(self, target_stress, target_pos):
        if target_pos not in self.words_by_stress_then_speech_part[target_stress]:
            # Correct POS not mandatory - just matching scansion is a good fallback!
            # TODO: Randomise rather than always taking first matching POS
            first_valid_pos = next(iter(self.words_by_stress_then_speech_part[target_stress]))
            target_pos = first_valid_pos
        valid_words = self.words_by_stress_then_speech_part[target_stress][target_pos]
        if len(valid_words) == 0:
            raise Exception(f'No valid words found with target stress: {target_stress} and pos: {target_pos}')
        return random.choice(valid_words)
