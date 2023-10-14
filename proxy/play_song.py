import xml.etree.ElementTree as ET

from karafun_parser import extract_data
from karafun_writer import write_parody_to_karafun
from generate_parody import generate_parody


def handle_play_song(flow, log):
    text = flow.response.text
    root = ET.fromstring(text)

    kf_data = extract_data(root)
    parody = generate_parody(kf_data, log)
    write_parody_to_karafun(kf_data, parody)
    final = ET.tostring(root, "unicode")
    flow.response.text = final
