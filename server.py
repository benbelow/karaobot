from flask import Flask
from flask import request
import json

from parody.generation.ParodyGenerator import generate_parody_with_line_ids, generate_parody

app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/parody', methods = ['POST'])
def generate_parody_with_ids():
    data = request.get_json()
    parody = generate_parody_with_line_ids(data)
    print(parody)
    return parody

@app.route('/parody/no-ids', methods = ['POST'])
def generate_parody_no_ids():
    data = request.get_data().decode("utf-8")
    parody = ""
    for line in generate_parody(data):
        parody += line
        parody += "\n"
    return parody



