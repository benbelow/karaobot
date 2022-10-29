from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship, backref
from .. import schema

Base = declarative_base()


class Word(Base):
    __tablename__ = 'Words'

    word = Column(String, primary_key=True)
    stress = Column(String)
    part_of_speech = Column(String)

    rhymes = relationship("Word",
                          secondary=schema.rhymes,
                          primaryjoin=word == schema.rhymes.c.word1,
                          secondaryjoin=word == schema.rhymes.c.word2,
                          lazy=False
                          )


class WordRhyme(Base):
    __tablename__ = 'WordRhymes'
    id = Column(Integer, primary_key=True)
    word1 = Column(String, ForeignKey("Words.word"))
    word2 = Column(String, ForeignKey("Words.word"))
    score = Column(Integer)
