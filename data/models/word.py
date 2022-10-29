from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy.orm.exc import DetachedInstanceError

from parody.analysis.AnalysedWord import AnalysedWord
from .. import schema

Base = declarative_base()


class Word(Base):
    __tablename__ = 'Words'

    word = Column(String, primary_key=True)
    stress = Column(String)
    part_of_speech = Column(String)

    rhymes = relationship("WordRhyme")

    def get_rhymes(self):
        try:
            return [r for r in self.rhymes]
        # TODO: Ew this is hacky, work out a better way of dealing with lazy loading
        except DetachedInstanceError as e:
            return None

    def analysedWord(self):
        return AnalysedWord(raw_word=self.word, part_of_speech=self.part_of_speech, stress=self.stress)


class WordRhyme(Base):
    __tablename__ = 'WordRhymes'
    id = Column(Integer, primary_key=True)
    word1 = Column(String, ForeignKey("Words.word"))
    word2 = Column(String)
    score = Column(Integer)
