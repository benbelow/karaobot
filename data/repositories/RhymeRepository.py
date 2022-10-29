import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class RhymeRepository:
    def __init__(self):
        db_uri = os.getenv('DB_URI')
        self.engine = create_engine(db_uri)

    def bulk_insert_rhymes(self, rhymes):
        with Session(self.engine) as session:
            session.bulk_save_objects(rhymes)
            session.commit()
