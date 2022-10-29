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

    def get_word(self, word):
        with Session(self.engine) as session:
            db_word = session.query(Word).options(joinedload(Word.rhymes)).get(word)
            return db_word

    def get_words(self, words):
        with Session(self.engine) as session:
            query = session.query(Word).options(joinedload(Word.rhymes))
            db_words = query.filter(Word.word.in_(words))
            return [w for w in db_words]
