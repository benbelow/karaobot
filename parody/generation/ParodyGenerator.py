import random

import prosodic as prosodic

from parody.generation.Corpus import Corpus, WordGenOptions

corpus = Corpus()

word_cache = {}
line_cache = {}


def generate_parody(lyrics):
    lines = str.splitlines(lyrics)
    for line in lines:
        parody_line = generate_parody_line(line)
        yield parody_line


def generate_parody_line(line):
    if line in line_cache:
        return line_cache[line]

    prosodic_text = prosodic.Text(line)
    prosodic_stanza = prosodic_text.children[0]
    prosodic_line = prosodic_stanza.children[0]
    prosodic_words = prosodic_line.children

    target_stresses = prosodic_line.str_stress()
    last_word = prosodic_words[-1]

    line = ""
    for prosodic_word in prosodic_words[0:len(prosodic_words) - 1]:
        if prosodic_word.token in word_cache:
            parody_word = word_cache[prosodic_word.token]
        else:
            target_stress = prosodic_word.stress
            parody_word = corpus.get_word(WordGenOptions(original=prosodic_word.token, target_stress=target_stress))
            word_cache[prosodic_word.token] = parody_word

        line = line + " " + parody_word.rawWord

    if last_word.token in word_cache:
        final_word = word_cache[last_word.token]
    else:
        options = WordGenOptions(original=last_word.token, target_stress=last_word.stress, rhyme_with=last_word.token)
        final_word = corpus.get_word(options)
        word_cache[last_word.token] = final_word

    line = line + " " + final_word.rawWord

    line_cache[line] = line
    return line
