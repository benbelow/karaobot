"""
Run as follows: mitmproxy -s karafun.py
"""
from mitmproxy import ctx
import xml.etree.ElementTree as ET

class Karafun:
    # Intercept all responses
    # API docs: https://docs.mitmproxy.org/stable/api/mitmproxy/http.html#HTTPFlow
    def response(self, flow):
        request_path = flow.request.path

        # Only modify the lyrics
        if "request.php" in request_path:

            text = flow.response.text
            root = ET.fromstring(text)

            karaoke = [x for x in root if x.tag == "karaoke"][0]
            pages = [x for x in karaoke if x.tag == "page"]

            for page in pages:
                lines = [x for x in page if x.tag == "line"]
                for line in lines:
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

            print("DONE")

            final = ET.tostring(root, "unicode")

            f = open("output.txt", "a")
            f.write(final)
            f.close()

            flow.response.text = final
            # TODO: interpret response XML, replace words and reconstruct

addons = [Karafun()]