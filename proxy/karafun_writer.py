def write_parody_to_karafun(kf_data, parody):
    """
    Updates data IN PLACE within kf_data.
    :param kf_data:
    :param parody:
    :return:
    """
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
