from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

quote_tag_table = Table(
    'quote_tag', Base.metadata,
    Column('quote_id', Integer, ForeignKey('quotes.quote.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('quotes.tag.id'), primary_key=True),
    schema='quotes'
)

class Author(Base):
    __tablename__ = 'author'
    __table_args__ = {'schema': 'quotes'}
    id = Column(Integer, primary_key=True, index=True)
    author = Column(String, index=True, unique=True, nullable=False)
    about = Column(Text, index=True)

    quotes = relationship('Quote', back_populates='author')

class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = {'schema': 'quotes'}
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, index=True, unique=True, nullable=False)

    quotes = relationship('Quote', secondary=quote_tag_table, back_populates='tags')

class Quote(Base):
    __tablename__ = 'quote'
    __table_args__ = {'schema': 'quotes'}
    id = Column(Integer, primary_key=True, index=True)
    quote = Column(Text, index=True, nullable=False)
    author_id = Column(Integer, ForeignKey('quotes.author.id'), nullable=False)

    author = relationship('Author', back_populates='quotes')
    tags = relationship('Tag', secondary=quote_tag_table, back_populates='quotes')
    