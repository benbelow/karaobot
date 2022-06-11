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
    target_stresses = prosodic_text.children[0].children[0].str_stress()

    last_word = prosodic_text.children[0].children[0].children[-1].token

    line = ""

    while len(target_stresses) != 0:
        syllables = min(random.choice([1]), len(target_stresses))
        target_stress = target_stresses[0:syllables]
        remaining_stress = target_stresses[syllables:]
        target_stresses = target_stresses[syllables:]

        should_rhyme = len(remaining_stress) == 0
        rhyme_with = last_word if should_rhyme else None

        parody_word = corpus.get_word(WordGenOptions(target_stress=target_stress, rhyme_with=rhyme_with))
        line = line + " " + parody_word.rawWord

    return line