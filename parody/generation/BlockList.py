blocked_words = []
bad_words = []

# These words are offensive and should never be shown
with open("data/source_data/blocklist.txt", 'r') as bad_list:
    lines = bad_list.readlines()
    for line in lines:
        blocked_words.append(line.strip())

# These words aren't offensive, but are rubbish words.
with open("data/source_data/badlist.txt", 'r') as bad_list:
    lines = bad_list.readlines()
    for line in lines:
        blocked_words.append(line.strip())


# TODO: Make this pre-selection, so we don't fall back to the original words
def enforce_blocklist(parody_word, original):
    return original if (parody_word in blocked_words or parody_word in bad_words) else parody_word
