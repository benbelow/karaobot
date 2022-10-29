import nltk as nltk
import prosodic as prosodic

from parody.analysis.AnalysedWord import analyse_word
from parody.generation.Corpus import Corpus, WordGenOptions

corpus = Corpus()

word_cache = {}
line_cache = {}


def generate_parody(lyrics):
    lines = str.splitlines(lyrics)
    for line in lines:
        parody_line = generate_parody_line(line)
        yield parody_line


def generate_parody_with_line_ids(lyrics):
    parody = {}

    for line_id in lyrics:
        parody_line = generate_parody_line(lyrics[line_id])
        parody[line_id] = parody_line.strip()
    return parody


def generate_parody_line(line):
    line = line.lower()
    if len(line) == 0:
        return ''
    if line in line_cache:
        return line_cache[line]

    # TODO: It would be nice to keep punctuation in, but for now it is treated as a whole word and so leaves off the end - fix later
    line = line.replace(",", "")
    line = line.replace(".", "")
    line = line.replace(":", "")
    line = line.replace(";", "")

    prosodic_text = prosodic.Text(line)
    prosodic_stanza = prosodic_text.children[0]
    prosodic_line = prosodic_stanza.children[0]
    prosodic_words = prosodic_line.children

    target_stresses = prosodic_line.str_stress()
    last_word = prosodic_words[-1]

    line = ""

    # TODO: Sort out apostrophes! It currently adds far too many syllables!

    for prosodic_word in prosodic_words[0:len(prosodic_words) - 1]:
        # TODO: Make this more resilient to all punctuations
        if prosodic_word.token == ",":
            parody_word = analyse_word(prosodic_word.token)
        elif prosodic_word.token in word_cache:
            parody_word = word_cache[prosodic_word.token]
        else:
            target_stress = prosodic_word.stress
            target_pos = get_pos(prosodic_word.token)
            gen_options = WordGenOptions(original=prosodic_word.token,
                                         target_stress=target_stress,
                                         target_pos=target_pos)
            parody_word = corpus.get_word(gen_options)
            word_cache[prosodic_word.token] = parody_word

        line = line + " " + parody_word.rawWord

    if last_word.token in word_cache:
        final_word = word_cache[last_word.token]
    else:
        # TODO: Look up words in database to avoid re-processing words we know
        options = WordGenOptions(
            original=last_word.token,
            target_stress=last_word.stress,
            target_pos=get_pos(last_word.token),
            rhyme_with=last_word.token)
        final_word = corpus.get_word(options)
        word_cache[last_word.token] = final_word

    line = line + " " + final_word.rawWord

    line_cache[line] = line
    return line


def get_pos(word):
    tokenized = nltk.word_tokenize(word)
    return nltk.pos_tag(tokenized)[0][1]
