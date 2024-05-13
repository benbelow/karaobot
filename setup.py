from data.repositories.wordRepository import WordRepository
from parody.analysis.WordImporter import import_words
import os



import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

repo = WordRepository()

use_lyrics = False

if use_lyrics:
    # TODO: some words are lazily added - better to make the bulk insert a bulk insert (if not exist) than wipe words here
    repo.delete_all_words()

    folder_path = "data/source_data/lyrics"
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                lines = file.readlines()
                import_words(lines)

else:
    with open("data/source_data/english_words_58_000.txt", 'r') as words_file:
        # TODO: some words are lazily added - better to make the bulk insert a bulk insert (if not exist) than wipe words here
        repo.delete_all_words()
        lines = words_file.readlines()
        import_words(lines)

