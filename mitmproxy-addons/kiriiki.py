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
                        for syllable in syllables:
                            text = [x for x in syllable if x.tag == "text"][0]
                            text.text = text.text.replace("a", "i").replace("e", "i").replace("o", "i").replace("u", "i")

            print("DONE")

            final = ET.tostring(root, "unicode")

            f = open("output.txt", "a")
            f.write(final)
            f.close()

            flow.response.text = final
            # TODO: interpret response XML, replace words and reconstruct

addons = [Karafun()]