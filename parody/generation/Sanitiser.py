def remove_special_characters(line):
    # TODO: It would be nice to keep punctuation in, but for now it is treated as a whole word and so leaves off the end
    line = line.replace(",", "")
    line = line.replace(".", "")
    line = line.replace(":", "")
    line = line.replace(";", "")
    line = line.replace("?", "")
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace("[", "")
    line = line.replace("]", "")
    line = line.replace("{", "")
    line = line.replace("}", "")
    line = line.replace("!", "")
    line = line.replace("\"", "")
    return line
