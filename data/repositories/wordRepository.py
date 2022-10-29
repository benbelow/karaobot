import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload

from data.models.word import Word


class WordRepository:
    def __init__(self):
        db_uri = os.getenv('DB_URI')
        self.engine = create_engine(db_uri)

    def delete_all_words(self):
        with Session(self.engine) as session:
            session.query(Word).delete()
            session.commit()

    def bulk_insert_words(self, words):
        with Session(self.engine) as session:
            session.bulk_save_objects(words)
            session.commit()

    def fetch_all_words(self):
        with Session(self.engine) as session:
            return session.query(Word)

    def query_words(self, session, load_rhymes):
        return session.query(Word).options(joinedload(Word.rhymes)) \
            if load_rhymes \
            else session.query(Word)

    def get_word(self, word, load_rhymes=False):
        with Session(self.engine) as session:
            db_word = self.query_words(session, load_rhymes).get(word)
            return db_word

    def get_words(self, words, load_rhymes=False):
        with Session(self.engine) as session:
            db_words = self.query_words(session, load_rhymes).filter(Word.word.in_(words))
            return [w for w in db_words]
