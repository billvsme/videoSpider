# -*- coding: utf-8 -*-
from sqlalchemy import (Column, Integer, BigInteger, String, Boolean, DateTime,
                        ForeignKey)
from ..medium import Medium


class Book(Medium):
    __tablename__ = 'books'

    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    alt_title = Column(String)
    isbn10 = Column(String)
    isbn13 = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'books',
    }
