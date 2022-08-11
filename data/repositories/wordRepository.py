import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from data.models.word import Word


class WordRepository:
    def __init__(self):
        db_uri = os.getenv('DB_URI')
        self.engine = create_engine(db_uri)

    def bulk_insert_words(self, words):
        with Session(self.engine) as session:
            session.query(Word).delete()
            session.bulk_save_objects(words)
            session.commit()
