import random

from parody.analysis.WordAnalyser import analyse_word, nlp, analyse_sentence

from data.repositories.wordRepository import WordRepository
from parody.analysis.WordImporter import import_words
from parody.generation.WordLookup import lookup_words
from stopwatch import Stopwatch

nlp.tokenizer.rules = {key: value for key, value in nlp.tokenizer.rules.items() if
                       "'" not in key and "’" not in key and "‘" not in key}


repo = WordRepository()

spooky_phrases_by_stress = {}

def import_words_from_phrases(lines):
    import_words(lines)


def all_words_in_lines(lines):
    words = []
    for line in lines:
        sentence = nlp(line)
        for word in sentence:
            words.append(word)
    return words


def stress_for_line(line):
    line = line.strip()
    tokens = nlp(line)
    line_words = [t.text.lower() for t in tokens if not t.text.isspace()]

    line_words = [l for l in line_words if l not in ['\'s']]

    word_lookup = lookup_words(line_words, Stopwatch())
    line_stress = ""
    for word in line_words:
        if word in word_lookup:
            orm_word = word_lookup[word]
            line_stress += orm_word.stress
    return line_stress


with open("data/source_data/spooky_phrases.txt", 'r') as block_file:
    lines = block_file.readlines()

    import_words_from_phrases(lines)
    # Go to the database for scansion to allow for custom scansions.
    # e.g. "Memebot" won't be recognised by Prosodic - but we can update the db manually to ensure it is recognised

    for line in lines:
        # doing this per line is probably slow. lookup_all_words does rhymes though which is definitely slower. Revisit
        line_stress = stress_for_line(line)
        if line_stress not in spooky_phrases_by_stress.keys():
            spooky_phrases_by_stress[line_stress] = []
        spooky_phrases_by_stress[line_stress].append(line)


def replace_with_custom_line(line):
    line_stress = stress_for_line(line)
    if line_stress in spooky_phrases_by_stress.keys():
        return random.choice(spooky_phrases_by_stress[line_stress])

    return None
