"""
Run as follows: mitmproxy -s karafun.py
"""
from mitmproxy import ctx
import xml.etree.ElementTree as ET
import requests

class Karafun:
    # Intercept all responses
    # API docs: https://docs.mitmproxy.org/stable/api/mitmproxy/http.html#HTTPFlow
    def response(self, flow):
        log = open("log.txt", "a")

        request_path = flow.request.path

        # Only modify the lyrics
        if "request.php" in request_path:

            text = flow.response.text
            root = ET.fromstring(text)

            original_lyrics = ""
            original_lyrics_by_line_id = {}

            karaoke = [x for x in root if x.tag == "karaoke"][0]
            pages = [x for x in karaoke if x.tag == "page"]

            for page in pages:
                lines = [x for x in page if x.tag == "line"]
                for line in lines:
                    line_id = int(line.get("id"))
                    if line_id not in original_lyrics_by_line_id:
                        original_lyrics_by_line_id[line_id] = ""
                    words = [x for x in line if x.tag == "word"]
                    for word in words:

                        syllables = [x for x in word if x.tag == "syllabe"]
                        start = syllables[0].find("start").text
                        end = syllables[-1].find("end").text
                        full_word = "".join([s.find("text").text for s in syllables])

                        for si in range(len(syllables)):
                            word.remove(syllables[si])

                        newSyllable = ET.Element("syllabe")
                        newStart = ET.Element("start")
                        newStart.text = start
                        newEnd = ET.Element("end")
                        newEnd.text = end
                        newText = ET.Element("text")
                        newText.text = full_word
                        newSyllable.append(newStart)
                        newSyllable.append(newEnd)
                        newSyllable.append(newText)

                        word.append(newSyllable)

                        original_lyrics += full_word
                        original_lyrics += " "
                        original_lyrics_by_line_id[line_id] += full_word
                        original_lyrics_by_line_id[line_id] += " "
                    original_lyrics += "\n"

            for k in original_lyrics_by_line_id:
                log.write(str(k))
                log.write(":")
                log.write(original_lyrics_by_line_id[k])
                log.write("\n")
            try:
                # TODO: Fix external (actually internal?) dependencies in mitmproxy
                parody = requests.post("http://localhost:5000/parody", json= original_lyrics_by_line_id).json()

            except Exception as e:
                log.write(e)

            for ip, page in enumerate(pages):
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


addons = [Karafun()]
