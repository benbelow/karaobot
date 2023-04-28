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
    nltk_part_of_speech = Column(String)
    spacy_part_of_speech = Column(String)
    spacy_morph = Column(String)

    rhymes = relationship("WordRhyme")

    def get_rhymes(self):
        try:
            return [r for r in self.rhymes]
        # TODO: Ew this is hacky, work out a better way of dealing with lazy loading
        except DetachedInstanceError as e:
            return None

    def analysed_word(self):
        return AnalysedWord(
            raw_word=self.word,
            nltk_part_of_speech=self.nltk_part_of_speech,
            stress=self.stress,
            spacy_pos=self.spacy_part_of_speech,
            spacy_morph=self.spacy_morph)


class WordRhyme(Base):
    __tablename__ = 'WordRhymes'
    id = Column(Integer, primary_key=True)
    word1 = Column(String, ForeignKey("Words.word"))
    word2 = Column(String)
    score = Column(Integer)
