from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from .subject import Subject


class Book(Subject):
    __tablename__ = 'books'

    id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
    alt_title = Column(String)
    isbn10 = Column(String)
    isbn13 = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'boos',
    }
