from data.repositories.wordRepository import WordRepository
from parody.analysis.WordImporter import import_words

repo = WordRepository()

with open("data/source_data/english_words_58_000.txt", 'r') as stop_words_file:
    # TODO: some words are lazily added - better to make the bulk insert a bulk insert (if not exist) than wipe words here
    repo.delete_all_words()
    lines = stop_words_file.readlines()
    import_words(lines)
