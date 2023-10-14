from xml.etree import ElementTree as ET

class KarafunData:
    token_field = 1

def extract_data(root):
    """
    Given an XML object from Karafun containing karaoke lyric data, extracts the lyrics from the XML
    and converts to a raw multi-line string
    :param root: root xml element of the data returned from Karafun
    :return: A single string with all the lyrics from the song
    """
    original_lyrics = ""

    data = KarafunData()
    data.original_lyrics_by_line_id = {}

    song = [x for x in root if x.tag == "song"][0]
    data.title = [x for x in song if x.tag == "title"][0].text
    data.artist = [x for x in song if x.tag == "artist"][0].text
    karaoke = [x for x in root if x.tag == "karaoke"][0]
    data.pages = [x for x in karaoke if x.tag == "page"]
    for page in data.pages:
        lines = [x for x in page if x.tag == "line"]
        for line in lines:
            line_id = int(line.get("id"))
            if line_id not in data.original_lyrics_by_line_id:
                data.original_lyrics_by_line_id[line_id] = ""

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
                data.original_lyrics_by_line_id[line_id] += full_word
                data.original_lyrics_by_line_id[line_id] += " "
            original_lyrics += "\n"
    # for k in original_lyrics_by_line_id:
    #     log.write(str(k))
    #     log.write(":")
    #     log.write(original_lyrics_by_line_id[k])
    #     log.write("\n")

    return data
