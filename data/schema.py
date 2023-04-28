import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy_utils import database_exists, create_database

db_uri = os.getenv('DB_URI')
print(db_uri)
engine = create_engine(db_uri)

if not database_exists(engine.url):
    print("creating db")
    create_database(engine.url)

# Create a metadata instance
metadata = MetaData(engine)
# Declare a table
words = Table('Words', metadata,
              Column('word', String, primary_key=True),
              Column('stress', String),
              Column('nltk_part_of_speech', String),
              Column('spacy_part_of_speech', String),
              Column('spacy_morph', String),
              )

rhymes = Table('WordRhymes', metadata,
               Column('id', Integer, primary_key=True),
               Column('word1', String, ForeignKey("Words.word")),
               Column('word2', String),
               Column('score', Integer)
               )

# This is happening every time the API is called! Extract to a migrations script only!
# Create all tables
metadata.create_all()
# for _t in metadata.tables:
#     print("Table: ", _t)
