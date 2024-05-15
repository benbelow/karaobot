from flask import Flask, abort
from flask import request
import json

from data.repositories.wordRepository import WordRepository
from parody.analysis.RhymeFinder import import_rhymes
from parody.generation.ParodyGenerator import generate_parody_with_line_ids, generate_parody, \
    generate_parody_from_metadata, generate_fully_rhyming_parody

HEADER_ARTIST = 'Karafun-Artist'
HEADER_TITLE = 'Karafun-Title'

app = Flask(__name__)

repo = WordRepository()
title_cache = {}


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/parody', methods=['POST'])
def generate_parody_with_ids():
    data = request.get_json()
    artist = request.headers.get(HEADER_ARTIST)
    title = request.headers.get(HEADER_TITLE)
    parody_title = title_cache[title] if title in title_cache.keys() else None;
    parody = generate_parody_with_line_ids(data, artist, title, parody_title)
    print(parody)
    return parody


@app.route('/parody/no-ids', methods=['POST'])
def generate_parody_no_ids():
    data = request.get_data().decode("utf-8")
    artist = request.headers.get('Karafun-Artist')
    title = request.headers.get('Karafun-Title')
    parody = ""
    for line in generate_parody(data, artist, title):
        parody += line
        parody += "\n"
    return parody



@app.route('/parody/title', methods=['POST'])
def generate_parody_title():
    data = request.get_data().decode("utf-8")
    artist = request.headers.get('Karafun-Artist')
    title = request.headers.get('Karafun-Title')

    if title in title_cache.keys():
        return title_cache[title]
    parody = ""
    for line in generate_fully_rhyming_parody(data, artist, title):
        parody += line
        parody += "\n"
    title_cache[title] = parody
    return parody


@app.route('/parody/from-metadata', methods=['POST'])
def generate_parody_from_metadata_http():
    data = request.get_data().decode("utf-8")
    metadata = json.loads(data)
    parody = ""
    for line in generate_parody_from_metadata(metadata["Artist"], metadata["Title"]):
        parody += line
        parody += "\n"
    return parody


@app.route('/words/<word>', methods=['GET'])
def get_word(word):
    db_word = repo.get_word(word, load_rhymes=True)
    if not db_word:
        abort(404)

    if not db_word.rhymes:
        import_rhymes(db_word)
        db_word = repo.get_word(word, load_rhymes=True)

    return json.dumps({
        'word': db_word.word,
        'stress': db_word.stress,
        'part_of_speech': db_word.part_of_speech,
        'rhymes': [r.word2 for r in db_word.rhymes]
    })
