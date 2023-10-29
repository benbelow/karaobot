import random

from parody.singleton import corpus
from similarity.client import get_similar_words

themes = []

with open("data/source_data/themes.txt", 'r') as block_file:
    lines = block_file.readlines()
    themes = [l.strip() for l in lines]


def pick_theme(artist, title):
    theme = random.choice(themes)

    theme_pos = [theme]
    theme_words = get_similar_words(theme_pos, [], 300)
    corpus.set_theme(artist, title, theme_words)
    print("CHOSEN THEME: " + theme + '\n')


def validate_themes():
    for theme in themes:
        theme_words = get_similar_words([theme], [], 300)
        theme_words = [t for t in theme_words if '_' not in t]
        print('THEME: ' + theme + ' Words: ' + str(len(theme_words)) + '\n')

