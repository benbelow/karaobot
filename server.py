from flask import Flask
from flask import request
import json

from parody.generation.ParodyGenerator import generate_parody_with_line_ids


app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/parody', methods = ['POST'])
def parody():
    data = request.get_json()
    parody = generate_parody_with_line_ids(data)
    return parody