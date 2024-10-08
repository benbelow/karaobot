from parody.analysis.RhymeFinder import import_rhymes
from parody.analysis.WordAnalyser import nlp
from parody.analysis.WordImporter import import_words
from parody.generation.Sanitiser import remove_special_characters
from parody.singleton import repo

excluded_from_rhymes = ['\'']

nlp.tokenizer.rules = {key: value for key, value in nlp.tokenizer.rules.items() if
                       "'" not in key and "’" not in key and "‘" not in key}


def lookup_all_words(lines):
    """
        Given a set of lines, extracts all words from each line, and performs a lookup.
        * Imports new words
        * Imports rhymes for words with none
        * Fetches word data PLUS rhymes from DB
        :param lines:
        :return: dictionary of word -> word with analysis + rhymes
        """
    # tokenise here so that cache and lookup for last words agree on what the last word is.
    # Otherwise problematic in cases where one word split by spaces but two words by tokens - e.g. gotta -> got ta & gotta
    tokenised_lines = [nlp(remove_special_characters(l)) for l in lines if l]
    words = [w.text.lower() for l in tokenised_lines if l for w in l]
    words = list(set(words))
    orm_words = repo.get_words(words, load_rhymes=True)

    new_words = list(set(words) - set([w.word for w in orm_words]))

    if new_words:
        import_words(w for w in new_words)

        new_orm_words = repo.get_words(new_words)
        orm_words = orm_words + new_orm_words

    have_rhymes = [n for n in orm_words if n.get_rhymes()]
    needing_rhymes = set([n for n in orm_words 
                          if n.word not in excluded_from_rhymes 
                          and not n.get_rhymes()])
    print("About to lookup rhymes: x" + len(needing_rhymes).__str__())

    if len(needing_rhymes) > 50:
        print('This song has too many rhymes to fetch, please skip!')
        # Sometimes genius thinks there's far too many lyrics and we start getting rate limited on rhyming -
        # mostly these are easier to just ignore the initial pre-load for
        raise Exception

    rhyme_import_count = 0
    for lw in needing_rhymes:
        import_rhymes(lw)
        rhyme_import_count = rhyme_import_count + 1
        print('RHYME IMPORT: ' + str(rhyme_import_count) + '/' + str(len(needing_rhymes)))

    newly_added_rhymes = repo.get_words([w.word for w in needing_rhymes], load_rhymes=True)
    orm_words = have_rhymes + newly_added_rhymes

    word_dict = {lw.word: lw for lw in orm_words}
    return word_dict

# Horrible duplication here with lookup all words, please fix
def lookup_last_words(lines):
    """
    Given a set of lines, extracts the last word from each line, and performs a lookup.
    * Imports new words
    * Imports rhymes for words with none
    * Fetches word data PLUS rhymes from DB
    :param lines:
    :return: dictionary of word -> word with analysis + rhymes
    """
    # tokenise here so that cache and lookup for last words agree on what the last word is.
    # Otherwise problematic in cases where one word split by spaces but two words by tokens - e.g. gotta -> got ta & gotta
    tokenised_lines = [nlp(remove_special_characters(l)) for l in lines if l]
    last_words = [l[-1].text.lower() for l in tokenised_lines if l]
    last_words = list(set(last_words))
    orm_last_words = repo.get_words(last_words, load_rhymes=True)

    new_words = list(set(last_words) - set([w.word for w in orm_last_words]))

    if new_words:
        import_words(w for w in new_words)

        new_orm_last_words = repo.get_words(new_words)
        orm_last_words = orm_last_words + new_orm_last_words

    have_rhymes = [n for n in orm_last_words if n.get_rhymes()]
    needing_rhymes = set([n for n in orm_last_words if not n.get_rhymes()])
    print("About to lookup rhymes: x" + len(needing_rhymes).__str__())

    if len(needing_rhymes) > 50:
        print('This song has too many rhymes to fetch, please skip!')
        # Sometimes genius thinks there's far too many lyrics and we start getting rate limited on rhyming -
        # mostly these are easier to just ignore the initial pre-load for
        raise Exception

    rhyme_import_count = 0
    for lw in needing_rhymes:
        import_rhymes(lw)
        rhyme_import_count = rhyme_import_count + 1
        print('RHYME IMPORT: ' + str(rhyme_import_count) + '/' + str(len(needing_rhymes)))

    newly_added_rhymes = repo.get_words([w.word for w in needing_rhymes], load_rhymes=True)
    orm_last_words = have_rhymes + newly_added_rhymes

    last_word_dict = {lw.word: lw for lw in orm_last_words}
    return last_word_dict


def lookup_words(line_words, sw, load_rhymes=False):
    words_in_line = repo.get_words(line_words, load_rhymes)
    sw.split("Get Words In Line")
    new_words = list(set(line_words) - set([w.word for w in words_in_line]))
    if new_words:
        import_words(w for w in new_words)

        sw.split("Import Words")

        # Fetch again to get info for any newly imported words
        words_in_line = repo.get_words(line_words)
        sw.split("Get Words (again)")
    words_by_token = {w.word: w for w in words_in_line}
    return words_by_token
