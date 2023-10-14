import xml.etree.ElementTree as ET

import requests

from karafun_parser import extract_data
from karafun_writer import write_parody_to_karafun


def handle_play_song(flow, log):
    text = flow.response.text
    root = ET.fromstring(text)

    kf_data = extract_data(root)
    parody = generate_parody(kf_data, log)
    write_parody_to_karafun(kf_data, parody)
    final = ET.tostring(root, "unicode")
    flow.response.text = final


def generate_parody(kf_data, log):
    try:
        # TODO: Fix external (actually internal?) dependencies in mitmproxy
        parody = requests.post(
            "http://localhost:5000/parody",
            json=kf_data.original_lyrics_by_line_id,
            headers={"Karafun-Title": kf_data.title, "Karafun-Artist": kf_data.artist}
        ).json()

    except Exception as e:
        log.write(e)
    log_parody(kf_data, log, parody)
    return parody


def log_parody(kf_data, log, parody):
    log.write("++++++++++++++++++++++++++++++++++++++++++\n")
    log.write(kf_data.title + " - " + kf_data.artist + "\n")
    log.write("\n")
    for k in parody:
        log.write(parody[str(k)])
        log.write("\n")
