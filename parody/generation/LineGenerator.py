import random

from parody.analysis.WordAnalyser import analyse_word, nlp
from parody.config import CHANCE_OF_CUSTOM_LINE, CHANCE_OF_ALTERNATE_WORDCOUNT
from parody.generation.BlockList import enforce_blocklist
from parody.generation.Corpus import WordGenOptions
from parody.generation.CustomLineSubstitutor import replace_with_custom_line, stress_for_line
from parody.generation.Sanitiser import remove_special_characters
from parody.generation.WordLookup import lookup_words
from parody.singleton import cache, corpus
from stopwatch import Stopwatch
from utils.random_utils import chance

nlp.tokenizer.rules = {key: value for key, value in nlp.tokenizer.rules.items() if
                       "'" not in key and "’" not in key and "‘" not in key}


#this is experimental and dangerous, as we no longer have a fallback when no words can be found. If we randomly
#generate a rare or impossible stress chunk, we're a bit screwed
def generate_parody_line_with_alternate_wordcount(line, last_word_dict, artist, title):
    line = line.lower()
    if len(line) == 0:
        return ''
    line = remove_special_characters(line)

    context_id = (artist, title)

    possible_chunks = corpus.get_available_stress_chunks()

    tokens = nlp(line)
    line_words = [t.text for t in tokens if not t.text.isspace()]
    last_word = last_word_dict[line_words[-1]]

    line_stress = stress_for_line(line)
    chunks = []
    while len(line_stress) > 0:
        if len(line_stress) <= 4 and line_stress in possible_chunks:
            chunks.append(line_stress)
            line_stress = ''
        else:
            potential_chunks = [line_stress[0:i] for i in range(1,min(len(line_stress) -1, 4))]
            valid_chunks = [pc for pc in potential_chunks if pc in possible_chunks]
            if len(valid_chunks) == 0:
                return None
            sylls = len(random.choice(valid_chunks))
            chunks.append(line_stress[0:sylls])
            line_stress = line_stress[sylls:]

    line = ''

    # 'last word' is now 'last chunk' and should rhyme
    for chunk in chunks[0:len(chunks)-1]:
        gen_options = WordGenOptions(original='qq', target_stress=chunk)
        parody_word = corpus.get_word(gen_options, context_id)
        line = line + ' ' + enforce_blocklist(parody_word.rawWord, 'qq')

    options = WordGenOptions(
        original='qq',
        target_stress=chunks[-1],
        rhyme_with=last_word)
    final_word = corpus.get_word(options, context_id)

    line = line + " " + enforce_blocklist(final_word.rawWord, 'qq')
    if 'qq' in line:
        return None

    return line


def generate_parody_line(line, last_word_dict, artist, title, parody_title):
    title_lower_words = title.lower().split()
    parody_title_words = parody_title.lower().split()
    if chance(CHANCE_OF_CUSTOM_LINE):
        custom = replace_with_custom_line(line)
        if custom is not None:
            return custom

    if chance(CHANCE_OF_ALTERNATE_WORDCOUNT):
        new_line = generate_parody_line_with_alternate_wordcount(line, last_word_dict, artist, title)
        if new_line is not None:
            return new_line

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

    line_words = [t.text for t in tokens if not t.text.isspace()]

    words_by_token = lookup_words(line_words, sw)

    orm_line_words = [words_by_token[lw] for lw in line_words if not lw.isspace()]

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
        elif word.word in title_lower_words and parody_title is not None:
            index = title_lower_words.index(word.word)
            parody_word = analyse_word(parody_title_words[index])
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

    if line_words[-1] in last_word_dict:
        last_word = last_word_dict[line_words[-1]]
    else:
        last_word = tokens[-1]
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


# TODO: This is very copy pasted from generate line. This whole file could do with a refactor really
def generate_fully_rhyming_parody_line(line, last_word_dict, artist, title):
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

    line_words = [t.text for t in tokens if not t.text.isspace()]

    words_by_token = lookup_words(line_words, sw, load_rhymes=True)

    orm_line_words = [words_by_token[lw] for lw in line_words if not lw.isspace()]

    line = ""

    for token in tokens:
        word = words_by_token[token.text]
        options = WordGenOptions(
            original=word.word,
            target_stress=word.stress,
            target_pos=token.pos_,
            target_morph=token.morph.__str__(),
            rhyme_with=word)
        new_word = corpus.get_word(options, context_id)

        line = line + " " + enforce_blocklist(new_word.rawWord, token.text)

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
