from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from .subject import Subject


class Movie(Subject):
    __tablename__ = 'movies'

    id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
    subtype = Column(String)
    official_site = Column(String)
    imdb_number = Column(String)
    duration = Column(String)
    year = Column(String)
    types = Column(String)
    languages = Column(String)
    genres = Column(String)
    countries = Column(String)
    current_season = Column(Integer)
    photos = Column(String)
    playable = Column(Boolean)

    crawler_tag = Column(String)
    crawler_sort = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'movie',
    }
