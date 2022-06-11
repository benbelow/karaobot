import random

import prosodic as prosodic

from parody.generation.Corpus import Corpus, WordGenOptions

corpus = Corpus()


def generate_parody(lyrics):
    lines = str.splitlines(lyrics)
    for line in lines:
        yield generate_parody_line(line)


def generate_parody_line(line):
    prosodic_text = prosodic.Text(line)
    # TODO: Keep track of the original words, don't just extract stresses out of context - it would be nice to weight towards one to one mapping, though we shouldn't *ONLY* do one to one.
    prosodic_stanza = prosodic_text.children[0]
    prosodic_line = prosodic_stanza.children[0]
    prosodic_words = prosodic_line.children

    target_stresses = prosodic_line.str_stress()
    last_word = prosodic_words[-1]

    line = ""
    for prosodic_word in prosodic_words[0:len(prosodic_words) - 1]:
        target_stress = prosodic_word.stress

        parody_word = corpus.get_word(WordGenOptions(original=prosodic_word.token, target_stress=target_stress))
        line = line + " " + parody_word.rawWord

    final_word = corpus.get_word(
        WordGenOptions(original=last_word.token, target_stress=last_word.stress, rhyme_with=last_word.token))
    line = line + " " + final_word.rawWord

    return line
