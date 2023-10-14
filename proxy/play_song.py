import xml.etree.ElementTree as ET

import requests

from karafun_parser import extract_data


def handle_play_song(flow, log):
    text = flow.response.text
    root = ET.fromstring(text)
    kf_data = extract_data(root)
    try:
        # TODO: Fix external (actually internal?) dependencies in mitmproxy
        parody = requests.post(
            "http://localhost:5000/parody",
            json=kf_data.original_lyrics_by_line_id,
            headers={"Karafun-Title": kf_data.title, "Karafun-Artist": kf_data.artist}
        ).json()

    except Exception as e:
        log.write(e)
    log.write("++++++++++++++++++++++++++++++++++++++++++\n")
    log.write(kf_data.title + " - " + kf_data.artist + "\n")
    log.write("\n")
    for k in parody:
        log.write(parody[str(k)])
        log.write("\n")
    for ip, page in enumerate(kf_data.pages):
        lines = [x for x in page if x.tag == "line"]
        for il, line in enumerate(lines):
            line_id = int(line.get("id"))
            words = [x for x in line if x.tag == "word"]
            for iw, word in enumerate(words):
                # assume we already turned each word into a single syllable
                syllables = [x for x in word if x.tag == "syllabe"]
                word_syllable = syllables[0]

                parody_line = parody[str(line_id)]
                parody_words = parody_line.split(" ")
                new_word = parody_words[iw] if len(parody_words) > iw else "qq"
                new_word = "qq" if new_word == "" else new_word

                text = [x for x in word_syllable if x.tag == "text"][0]
                text.text = new_word
    final = ET.tostring(root, "unicode")
    flow.response.text = final
    # TODO: interpret response XML, replace words and reconstruct


