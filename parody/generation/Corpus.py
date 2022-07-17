import random
import csv
import nltk as nltk
from parody.analysis.AnalysedWord import AnalysedWord
from pyrhyme import rhyming_list


class WordGenOptions:
    def __init__(self, original, target_stress=None, rhyme_with=None, target_pos=None):
        self.original = original
        self.target_stress = target_stress
        self.rhyme_with = rhyme_with
        self.target_pos = target_pos


class Corpus:
    words_by_stress_then_speech_part = {}
    stop_words = []

    def __init__(self):
        with open("data/english-word-list-total.csv", 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile, delimiter=';')

            # extracting field names through first row
            fields = next(csvreader)

            # extracting each data row one by one
            for row in csvreader:
                raw_word = row[1]
                word = AnalysedWord(raw_word)
                stress = word.stress()
                pos = word.partOfSpeech

                if stress not in self.words_by_stress_then_speech_part:
                    self.words_by_stress_then_speech_part[stress] = {}
                if pos not in self.words_by_stress_then_speech_part[stress]:
                    self.words_by_stress_then_speech_part[stress][pos] = []

                self.words_by_stress_then_speech_part[stress][pos].append(word)

        with open("data/english_words_58_000.txt", 'r') as stop_words_file:
            lines = stop_words_file.readlines()

            i = 0
            for line in lines:
                i += 1
                if i % 1000 == 0:
                    print("imported: " + line)
                word = AnalysedWord(line.strip())
                stress = word.stress()
                pos = word.partOfSpeech

                if stress not in self.words_by_stress_then_speech_part:
                    self.words_by_stress_then_speech_part[stress] = {}
                if pos not in self.words_by_stress_then_speech_part[stress]:
                    self.words_by_stress_then_speech_part[stress][pos] = []

                self.words_by_stress_then_speech_part[stress][pos].append(word)

        with open("data/stop_words.txt", 'r') as stop_words_file:
            lines = stop_words_file.readlines()

            for line in lines:
                self.stop_words.append(line.strip())

    def get_word(self, generation_options):
        rhyme_with = generation_options.rhyme_with
        target_stress = generation_options.target_stress
        target_pos = generation_options.target_pos

        if len(target_stress) == 0:
            return AnalysedWord("")
        if generation_options.original in self.stop_words:
            return AnalysedWord(generation_options.original)
        if rhyme_with is not None:
            return self.get_rhyming_word(rhyme_with, target_stress, target_pos)
        if target_stress is not None:
            return self.get_stressed_word(target_stress, target_pos)

    def get_rhyming_word(self, rhyme_with, target_stress, target_pos):
        # TODO: This is calling an API under the hood, so it's quite the bottleneck. Try:
        #  (i) evaluate all the rhymes we want up-front
        #  (ii) Fetch them in parallel
        #  (iii) Check that the API's ok with the rate
        raw_rhymes = rhyming_list(rhyme_with, lang="en")
        # perfect rhymes only for now - TODO: Fallback to half rhymes.
        # TODO: Weight towards more common words for rhymes
        rhyming_words = [perfect_rhyme for perfect_rhyme in raw_rhymes if perfect_rhyme.score == 300]
        stressed_rhyming_words = [AnalysedWord(rhyme.word) for rhyme in rhyming_words]

        valid_rhyming_words = [word for word in stressed_rhyming_words if word.stress() == target_stress] \
            if target_stress is not None \
            else stressed_rhyming_words

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
