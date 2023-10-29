def write_parody_to_karafun(kf_data, parody):
    """
    Updates data IN PLACE within kf_data.
    :param kf_data:
    :param parody:
    :return:
    """
    for page_index, page in enumerate(kf_data.pages):
        lines = [x for x in page if x.tag == "line"]
        for il, line in enumerate(lines):
            line_id = int(line.get("id"))
            words = [x for x in line if x.tag == "word"]
            for word_index, word in enumerate(words):
                # assume we already turned each word into a single syllable
                syllables = [x for x in word if x.tag == "syllabe"]
                word_syllable = syllables[0]

                parody_line = parody[str(line_id)]
                parody_words = parody_line.split(" ")
                new_word = parody_words[word_index] if len(parody_words) > word_index else "."
                new_word = "?" if new_word == "" else new_word

                text = [x for x in word_syllable if x.tag == "text"][0]

                if word_index == len(words) - 1 and len(parody_words) > len(words):
                    for i in range(len(words), len(parody_words)):
                        new_word += "_"
                        new_word += parody_words[i]

                text.text = new_word
