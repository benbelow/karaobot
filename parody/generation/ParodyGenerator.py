import spacy

from parody.generation.LineGenerator import generate_parody_line, generate_fully_rhyming_parody_line
from parody.generation.WordLookup import lookup_last_words, lookup_all_words
from parody.singleton import cache, corpus
from similarity.client import get_similar_words

nlp = spacy.load("en_core_web_sm")

from genius_client.genius import fetch_lyrics
from stopwatch import Stopwatch


def generate_parody_from_metadata(artist, title):
    original_lyrics = fetch_lyrics(artist, title)
    parody = generate_parody(original_lyrics, artist, title)
    for parody_line in parody:
        yield parody_line
    # Don't clear cache, as this will be called in background, and we don't want to clear it mid-generation if someone
    # is queuing songs just as another hits the front of the queue
    # TODO: Cache per request scope, so we can clear again here
    # cache.clear()


def generate_fully_rhyming_parody(lyrics, artist, title):
    lines = str.splitlines(lyrics)
    sw = Stopwatch().start()

    last_word_dict = lookup_all_words(lines)
    sw.split("Get rhymes for *all* words")

    for line in lines:
        parody_line = generate_fully_rhyming_parody_line(line, last_word_dict, artist, title)
        sw.split("Line generation")
        yield parody_line
    cache.clear()


def generate_parody(lyrics, artist, title):
    lines = str.splitlines(lyrics)
    sw = Stopwatch().start()

    last_word_dict = lookup_last_words(lines)
    sw.split("Get rhymes for *all* last words")

    theme_pos = ["fish"]
    theme_words = get_similar_words(theme_pos, [], 300)
    corpus.set_theme(artist, title, theme_words)

    for line in lines:
        parody_line = generate_parody_line(line, last_word_dict, artist, title)
        sw.split("Line generation")
        yield parody_line
    cache.clear()


def generate_parody_with_line_ids(lyrics, artist, title):
    parody = {}

    lines = [lyrics[k] for k in lyrics]
    last_word_dict = lookup_last_words(lines)

    theme_pos = ["flamingo"]
    theme_words = get_similar_words(theme_pos, [], 300)
    corpus.set_theme(artist, title, theme_words)

    for line_id in lyrics:
        parody_line = generate_parody_line(lyrics[line_id], last_word_dict, artist, title)
        parody[line_id] = parody_line.strip()
    cache.clear()
    return parody
