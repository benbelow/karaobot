import nltk as nltk
import prosodic as prosodic

from data.repositories.wordRepository import WordRepository
from genius_client.genius import fetch_lyrics
from parody.analysis.AnalysedWord import analyse_word, AnalysedWord
from parody.analysis.RhymeFinder import import_rhymes
from parody.analysis.WordImporter import import_words
from parody.generation.Corpus import Corpus, WordGenOptions
from stopwatch import Stopwatch

blocked_words = []
bad_words = []

# These words are offensive and should never be shown
with open("data/source_data/blocklist.txt", 'r') as bad_list:
    lines = bad_list.readlines()
    for line in lines:
        blocked_words.append(line.strip())

# These words aren't offensive, but are rubbish words.
with open("data/source_data/badlist.txt", 'r') as bad_list:
    lines = bad_list.readlines()
    for line in lines:
        blocked_words.append(line.strip())


class Cache:
    rhyming_word_cache_by_metadata = {}
    word_cache_by_metadata = {}
    line_cache_by_metadata = {}

    def clear(self):
        self.rhyming_word_cache_by_metadata = {}
        self.word_cache_by_metadata = {}
        self.line_cache_by_metadata = {}

    def rhyming_word_cache(self, artist, title):
        artist = artist if artist else "Unknown"
        title = title if title else "Unknown"
        if artist not in self.rhyming_word_cache_by_metadata.keys():
            self.rhyming_word_cache_by_metadata[artist] = {}

        artist_cache = self.rhyming_word_cache_by_metadata[artist]

        if title not in artist_cache.keys():
            artist_cache[title] = {}
        return artist_cache[title]

    def word_cache(self, artist, title):
        artist = artist if artist else "Unknown"
        title = title if title else "Unknown"
        if artist not in self.word_cache_by_metadata.keys():
            self.word_cache_by_metadata[artist] = {}

        artist_cache = self.word_cache_by_metadata[artist]

        if title not in artist_cache.keys():
            artist_cache[title] = {}
        return artist_cache[title]

    def line_cache(self, artist, title):
        artist = artist if artist else "Unknown"
        title = title if title else "Unknown"
        if artist not in self.line_cache_by_metadata.keys():
            self.line_cache_by_metadata[artist] = {}

        artist_cache = self.line_cache_by_metadata[artist]

        if title not in artist_cache.keys():
            artist_cache[title] = {}
        return artist_cache[title]


corpus = Corpus()

cache = Cache()

repo = WordRepository()


def generate_parody_from_metadata(artist, title):
    original_lyrics = fetch_lyrics(artist, title)
    parody = generate_parody(original_lyrics, artist, title)
    for parody_line in parody:
        yield parody_line
    # Don't clear cache, as this will be called in background, and we don't want to clear it mid-generation if someone
    # is queuing songs just as another hits the front of the queue
    # TODO: Cache per request scope, so we can clear again here
    # cache.clear()


def generate_parody(lyrics, artist, title):
    lines = str.splitlines(lyrics)
    sw = Stopwatch().start()

    last_word_dict = lookup_last_words(lines)
    sw.split("Get rhymes for *all* last words")

    for line in lines:
        parody_line = generate_parody_line(line, last_word_dict, artist, title)
        sw.split("Line generation")
        yield parody_line
    cache.clear()


def generate_parody_with_line_ids(lyrics, artist, title):
    parody = {}

    lines = [lyrics[k] for k in lyrics]
    last_word_dict = lookup_last_words(lines)

    for line_id in lyrics:
        parody_line = generate_parody_line(lyrics[line_id], last_word_dict, artist, title)
        parody[line_id] = parody_line.strip()
    cache.clear()
    return parody


def lookup_last_words(lines):
    split_lines = [l.split() for l in lines if l]
    last_words = [remove_special_characters(l[-1].lower()) for l in split_lines if l]
    last_words = list(set(last_words))
    orm_last_words = repo.get_words(last_words, load_rhymes=True)

    new_words = list(set(last_words) - set([w.word for w in orm_last_words]))

    if new_words:
        import_words(w for w in new_words)

        new_orm_last_words = repo.get_words(new_words)
        orm_last_words = orm_last_words + new_orm_last_words

    have_rhymes = [n for n in orm_last_words if n.get_rhymes()]
    needing_rhymes = set([n for n in orm_last_words if not n.get_rhymes()])
    print("HOW MANY NEED RHYMES?")
    print(len(needing_rhymes))

    if len(needing_rhymes) > 50:
        # Somethimes genius thinks there's far too many lyrics and we start getting rate limited on rhyming - mostly these are easier to just ignore the initial pre-load for
        raise Exception

    for lw in needing_rhymes:
        import_rhymes(lw)

    newly_added_rhymes = repo.get_words([w.word for w in needing_rhymes], load_rhymes=True)
    orm_last_words = have_rhymes + newly_added_rhymes

    last_word_dict = {lw.word: lw for lw in orm_last_words}
    return last_word_dict


def generate_parody_line(line, last_word_dict, artist, title):
    line_cache = cache.line_cache(artist, title)
    word_cache = cache.word_cache(artist, title)
    rhyming_word_cache = cache.rhyming_word_cache(artist, title)

    line = line.lower()
    if len(line) == 0:
        return ''
    if line in line_cache:
        return line_cache[line]

    line = remove_special_characters(line)

    sw = Stopwatch().start()

    line_words = line.split()
    words_in_line = repo.get_words(line_words)

    sw.split("Get Words In Line")

    new_words = list(set(line_words) - set([w.word for w in words_in_line]))

    if new_words:
        import_words(w for w in new_words)

        sw.split("Import Words")

        # Fetch again to get info for any newly imported words
        words_in_line = repo.get_words(line_words)
        sw.split("Get Words (again)")

    words_by_token = {w.word: w for w in words_in_line}

    orm_line_words = [words_by_token[lw] for lw in line_words]

    line = ""

    # TODO: Sort out apostrophes! It currently adds far too many syllables!

    # Parody all but last word
    for word in orm_line_words[0:len(orm_line_words) - 1]:
        # TODO: Make this more resilient to all punctuations
        if word.word == ",":
            parody_word = analyse_word(word.word)
        elif word.word in word_cache:
            parody_word = word_cache[word.word]
        else:
            target_stress = word.stress
            target_pos = get_pos(word.word)
            gen_options = WordGenOptions(original=word.word,
                                         target_stress=target_stress,
                                         target_pos=target_pos)
            parody_word = corpus.get_word(gen_options)
            word_cache[word.word] = parody_word

        line = line + " " + enforce_blocklist(parody_word.rawWord, word.word)

    sw.split("Body Words")

    last_word = last_word_dict[line_words[-1]]

    # Parody last word
    # TODO: Lookahead to ensure all last words rhyme up front, rather than using different substitutions
    #  for mid/emd line versions of same word
    if last_word.word in rhyming_word_cache:
        final_word = rhyming_word_cache[last_word.word]
    else:
        options = WordGenOptions(
            original=last_word.word,
            target_stress=last_word.stress,
            target_pos=get_pos(last_word.word),
            rhyme_with=last_word)
        final_word = corpus.get_word(options)
        rhyming_word_cache[last_word.word] = final_word

    sw.split("Last Word")

    line = line + " " + enforce_blocklist(final_word.rawWord, last_word.word)

    line_cache[line] = line
    return line


def remove_special_characters(line):
    # TODO: It would be nice to keep punctuation in, but for now it is treated as a whole word and so leaves off the end - fix later
    line = line.replace(",", "")
    line = line.replace(".", "")
    line = line.replace(":", "")
    line = line.replace(";", "")
    line = line.replace("?", "")
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace("[", "")
    line = line.replace("]", "")
    line = line.replace("{", "")
    line = line.replace("}", "")
    line = line.replace("!", "")
    line = line.replace("\"", "")
    return line

# TODO: Make this pre-selection, so we don't fall back to the original words
def enforce_blocklist(parody_word, original):
    return original if (parody_word in blocked_words or parody_word in bad_words) else parody_word


def get_pos(word):
    tokenized = nltk.word_tokenize(word)
    return nltk.pos_tag(tokenized)[0][1]
