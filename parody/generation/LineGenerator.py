from parody.analysis.WordAnalyser import analyse_word, nlp
from parody.generation.BlockList import enforce_blocklist
from parody.generation.Corpus import WordGenOptions
from parody.generation.Sanitiser import remove_special_characters
from parody.generation.WordLookup import lookup_words
from parody.singleton import cache, corpus
from stopwatch import Stopwatch


def generate_parody_line(line, last_word_dict, artist, title):
    line_cache = cache.line_cache(artist, title)
    word_cache = cache.word_cache(artist, title)
    rhyming_word_cache = cache.rhyming_word_cache(artist, title)

    line = line.lower()
    if len(line) == 0:
        return ''
    if line in line_cache:
        return line_cache[line]

    line = remove_special_characters(line)

    tokens = nlp(line)

    sw = Stopwatch().start()

    line_words = [t.text for t in tokens]

    words_by_token = lookup_words(line_words, sw)

    orm_line_words = [words_by_token[lw] for lw in line_words]

    line = ""

    # TODO: Sort out apostrophes! It currently adds far too many syllables!

    # Parody all but last word
    for token in tokens[0:len(tokens) - 1]:
        word = words_by_token[token.text]
        # TODO: Make this more resilient to all punctuations
        if word.word == ",":
            parody_word = analyse_word(word.word)
        elif word.word in word_cache:
            parody_word = word_cache[word.word]
        else:
            target_stress = word.stress
            target_pos = token.pos_
            target_morph = token.morph.__str__()
            gen_options = WordGenOptions(original=word.word,
                                         target_stress=target_stress,
                                         target_pos=target_pos,
                                         target_morph=target_morph)
            parody_word = corpus.get_word(gen_options)
            word_cache[word.word] = parody_word

        line = line + " " + enforce_blocklist(parody_word.rawWord, word.word)

    sw.split("Body Words")

    last_word = last_word_dict[line_words[-1]]
    token = tokens[-1]

    # Parody last word
    # TODO: Lookahead to ensure all last words rhyme up front, rather than using different substitutions
    # for mid/emd line versions of same word
    if last_word.word in rhyming_word_cache:
        final_word = rhyming_word_cache[last_word.word]
    else:
        options = WordGenOptions(
            original=last_word.word,
            target_stress=last_word.stress,
            target_pos=token.pos_,
            target_morph=token.morph.__str__(),
            rhyme_with=last_word)
        final_word = corpus.get_word(options)
        rhyming_word_cache[last_word.word] = final_word

    sw.split("Last Word")

    line = line + " " + enforce_blocklist(final_word.rawWord, last_word.word)

    line_cache[line] = line
    return line


