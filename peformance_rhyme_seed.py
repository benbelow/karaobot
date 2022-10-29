from data.repositories.wordRepository import WordRepository
from parody.analysis.RhymeFinder import import_rhymes

repo = WordRepository()

with open("data/source_data/english_words_58_000.txt", 'r') as stop_words_file:
    lines = stop_words_file.readlines()
    db_words = repo.get_words([l.strip() for l in lines])
    to_import = [w for w in db_words if not w.rhymes]
    for word in to_import:
        import_rhymes(word)
