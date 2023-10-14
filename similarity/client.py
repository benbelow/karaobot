import requests


def get_similar_words(pos, neg, topn):
    parody = requests.post(
        "http://localhost:5001/most-similar",
        json={
            "pos": pos,
            "neg": neg,
            "topn": topn
        },
    ).json()

    return parody
