from flask import Flask, abort, jsonify, request

from similarity.Similar import most_similar

app = Flask(__name__)

@app.route('/')
def index():
    return 'Server Works!'


@app.route('/most-similar', methods=['POST'])
def generate_parody_with_ids():
    data = request.get_json()
    similar = most_similar(data["pos"], data["neg"], data["topn"])
    return jsonify([s[0] for s in similar])
