import os
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy_utils import database_exists, create_database

db_uri = os.getenv('DB_URI')
engine = create_engine(db_uri)

if not database_exists(engine.url):
    create_database(engine.url)

# Create a metadata instance
metadata = MetaData(engine)
# Declare a table
table = Table('Words', metadata,
              Column('id', Integer, primary_key=True),
              Column('word', String),
              Column('stress', String),
              Column('part_of_speech', String),
              )

# Create all tables
metadata.create_all()
for _t in metadata.tables:
    print("Table: ", _t)
