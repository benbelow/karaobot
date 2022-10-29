import nltk as nltk
import prosodic as prosodic

from data.repositories.wordRepository import WordRepository
from parody.analysis.AnalysedWord import analyse_word, AnalysedWord
from parody.analysis.WordImporter import import_words
from parody.generation.Corpus import Corpus, WordGenOptions

blocked_words = []

with open("data/source_data/blocklist.txt", 'r') as block_file:
    lines = block_file.readlines()
    for line in lines:
        blocked_words.append(line.strip())


class Cache:
    rhyming_word_cache = {}
    word_cache = {}
    line_cache = {}

    def clear(self):
        self.rhyming_word_cache = {}
        self.word_cache = {}
        self.line_cache = {}


corpus = Corpus()

cache = Cache()

repo = WordRepository()


def generate_parody(lyrics):
    lines = str.splitlines(lyrics)
    for line in lines:
        parody_line = generate_parody_line(line)
        yield parody_line
    cache.clear()


def generate_parody_with_line_ids(lyrics):
    parody = {}

    for line_id in lyrics:
        parody_line = generate_parody_line(lyrics[line_id])
        parody[line_id] = parody_line.strip()
    cache.clear()
    return parody


def generate_parody_line(line):
    line = line.lower()
    if len(line) == 0:
        return ''
    if line in cache.line_cache:
        return cache.line_cache[line]

    # TODO: It would be nice to keep punctuation in, but for now it is treated as a whole word and so leaves off the end - fix later
    line = line.replace(",", "")
    line = line.replace(".", "")
    line = line.replace(":", "")
    line = line.replace(";", "")
    line = line.replace("?", "")
    line = line.replace("?", "")
    line = line.replace("(", "")
    line = line.replace(")", "")

    line_words = line.split()
    words_in_line = repo.get_words(line_words)

    new_words = list(set(line_words) - set([w.word for w in words_in_line]))
    import_words(w for w in new_words)

    # Fetch again to get info for any newly imported words
    words_in_line = repo.get_words(line_words)
    words_by_token = {w.word: w for w in words_in_line}

    orm_line_words = [words_by_token[lw] for lw in line_words]
    last_word = orm_line_words[-1]

    line = ""

    # TODO: Sort out apostrophes! It currently adds far too many syllables!

    # Parody all but last word
    for word in orm_line_words[0:len(orm_line_words) - 1]:
        # TODO: Make this more resilient to all punctuations
        if word.word == ",":
            parody_word = analyse_word(word.word)
        elif word.word in cache.word_cache:
            parody_word = cache.word_cache[word.word]
        else:
            target_stress = word.stress
            target_pos = get_pos(word.word)
            gen_options = WordGenOptions(original=word.word,
                                         target_stress=target_stress,
                                         target_pos=target_pos)
            parody_word = corpus.get_word(gen_options)
            cache.word_cache[word.word] = parody_word

        line = line + " " + enforce_blocklist(parody_word.rawWord, word.word)

    # Parody last word
    # TODO: Lookahead to ensure all last words rhyme up front, rather than using different substitutions for mid/emd line versions of same word
    if last_word.word in cache.rhyming_word_cache:
        final_word = cache.rhyming_word_cache[last_word.word]
    else:
        options = WordGenOptions(
            original=last_word.word,
            target_stress=last_word.stress,
            target_pos=get_pos(last_word.word),
            rhyme_with=last_word)
        final_word = corpus.get_word(options)
        cache.rhyming_word_cache[last_word.word] = final_word

    line = line + " " + enforce_blocklist(final_word.rawWord, last_word.word)

    cache.line_cache[line] = line
    return line


def enforce_blocklist(parody_word, original):
    return original if parody_word in blocked_words else parody_word


def get_pos(word):
    tokenized = nltk.word_tokenize(word)
    return nltk.pos_tag(tokenized)[0][1]
