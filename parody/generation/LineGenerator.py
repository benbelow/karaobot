from parody.analysis.WordAnalyser import analyse_word, nlp
from parody.generation.BlockList import enforce_blocklist
from parody.generation.Corpus import WordGenOptions
from parody.generation.Sanitiser import remove_special_characters
from parody.generation.WordLookup import lookup_words
from parody.singleton import cache, corpus
from stopwatch import Stopwatch

nlp.tokenizer.rules = {key: value for key, value in nlp.tokenizer.rules.items() if
                       "'" not in key and "’" not in key and "‘" not in key}


def generate_parody_line(line, last_word_dict, artist, title):
    context_id = (artist, title)

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
        # Tokeniser from Spacy splits words liek 'Ben's' into 'Ben' and "'s" so it can correctly identify the 1st part.
        # We let it do its thing, then don't try to parody the possessive and add it back to the replacement later
        if word.word == "'s":
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
            parody_word = corpus.get_word(gen_options, context_id)
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
        final_word = corpus.get_word(options, context_id)
        rhyming_word_cache[last_word.word] = final_word

    sw.split("Last Word")

    line = line + " " + enforce_blocklist(final_word.rawWord, last_word.word)

    line = process_possessives(line)

    line_cache[line] = line
    return line


def process_possessives(input_string):
    input_strings = input_string.split()
    output_strings = []
    i = 0

    while i < len(input_strings):
        current_string = input_strings[i]
        if current_string == "'s":
            if i > 0:
                output_strings[-1] += current_string
        else:
            output_strings.append(current_string)

        i += 1

    return ' '.join(output_strings)