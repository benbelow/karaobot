"""
Run as follows: mitmproxy -s karafun.py
"""
from mitmproxy import ctx
import xml.etree.ElementTree as ET

from parody.generation.ParodyGenerator import generate_parody


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
                # TODO: Fix external dependencies in mitmproxy
                # parody = generate_parody(original_lyrics)
                parody = {1: "Yeah",
                          2: "It was",
                          3: "the auction",

                          4: "a plan",
                          5: "concoction",

                          6: "Believe",
                          7: "when I say",

                          8: "it's Carrot Cake Friday",

                          9: "Wendi's",
                          10: "bid not won",
                          11: "by⠀us",

                          12: "Cat paid for",
                          13: "a Vengabus",

                          14: "so I say",
                          15: "it's Gareth Cake Friday",

                          16: "Bake us cakes",
                          17: "ain't nothing but a good⠀bake",
                          18: "Bake us cakes",
                          19: "ain't no⠀chance of a mistake",
                          20: "Bake us cakes",
                          21: "I always wanna hear you say",
                          22: "it's Gareth Cake Friday",

                          23: "I'll watch",
                          24: "the livestream",
                          25: "our new",
                          26: "kitchen⠀team",
                          27: "For cupcakes",
                          28: "it's too late",

                          29: "still, Gareth Cake Friday",
                          30: "Bake us cakes",
                          31: "ain't nothing but a good⠀bake",
                          32: "Bake us cakes",
                          33: "ain't no⠀chance of a mistake",
                          34: "Bake us cakes",
                          35: "I never wanna hear you say",
                          36: "it's Gareth Cake Friday",

                          37: "Now I can see",
                          38: "that they're falling apart",
                          39: "Not the way",
                          40: "that they're meant to be yeah",

                          41: "No matter the texture",
                          42: "I want you to know",
                          43: "That he followed",
                          44: "the recipe",

                          45: "Fresh baked",
                          46: "in fire",
                          47: "Apron",
                          48: "attire",
                          49: "It's time",

                          50: "There's time⠀for one more cake",
                          51: "There's time⠀for one more cake",

                          52: "Oh yeah",

                          53: "Gareth Cake Friday",
                          54: "Bake us cakes",
                          55: "ain't nothing but a good⠀bake",
                          56: "Bake us cakes",
                          57: "ain't no⠀chance of a mistake",
                          58: "Bake us cakes",
                          59: "I always wanna hear you say",
                          60: "it's Gareth Cake Friday",

                          61: "Bake us cakes",
                          62: "ain't no⠀chance of a mistake",
                          63: "Bake us cakes",
                          64: "I always wanna hear you say",
                          65: "Gareth Cake Friday",
                          66: "It's Gareth Cake Friday"
                          }
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

                        parody_line = parody[line_id]
                        parody_words = parody_line.split(" ")
                        new_word = parody_words[iw] if len(parody_words) > iw else " "

                        text = [x for x in word_syllable if x.tag == "text"][0]
                        text.text = new_word

            final = ET.tostring(root, "unicode")
            flow.response.text = final
            # TODO: interpret response XML, replace words and reconstruct


addons = [Karafun()]
