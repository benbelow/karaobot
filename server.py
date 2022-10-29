from flask import Flask, abort
from flask import request
import json

from data.repositories.wordRepository import WordRepository
from parody.analysis.RhymeFinder import import_rhymes
from parody.generation.ParodyGenerator import generate_parody_with_line_ids, generate_parody

app = Flask(__name__)

repo = WordRepository()


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/parody', methods=['POST'])
def generate_parody_with_ids():
    data = request.get_json()
    parody = generate_parody_with_line_ids(data)
    print(parody)
    return parody


@app.route('/parody/no-ids', methods=['POST'])
def generate_parody_no_ids():
    data = request.get_data().decode("utf-8")
    parody = ""
    for line in generate_parody(data):
        parody += line
        parody += "\n"
    return parody


@app.route('/words/<word>', methods=['GET'])
def get_word(word):
    db_word = repo.get_word(word)
    if not db_word:
        abort(404)

    if not db_word.rhymes:
        db_word = import_rhymes(db_word)

    return json.dumps({
        'word': db_word.word,
        'stress': db_word.stress,
        'part_of_speech': db_word.part_of_speech,
        'rhymes': [r.word2 for r in db_word.rhymes]
    })
