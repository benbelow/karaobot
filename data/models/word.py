from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Word(Base):
    __tablename__ = 'Words'
    word = Column(String, primary_key=True)
    stress = Column(String)
    part_of_speech = Column(String)
