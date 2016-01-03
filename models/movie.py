from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from .subject import Subject


class Movie(Subject):
    __tablename__ = 'movies'

    id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
    aka = Column(String)
    alt = Column(String)
    mobile_url = Column(String)
    subtype = Column(String)
    website = Column(String)
    douban_site = Column(String)
    pubdates = Column(String)
    mainland_pubdate = Column(String)
    pubdate = Column(String)
    year = Column(String)
    languages = Column(String)
    durations = Column(String)
    genres = Column(String)
    countries = Column(String)
    comments_count = Column(Integer)
    reviews_count = Column(Integer)
    seasons_count = Column(Integer)
    current_season = Column(Integer)
    current_season = Column(Integer)
    schedule_url = Column(String)
    trailer_urls = Column(String)
    clip_urls = Column(String)
    blooper_urls = Column(String)
    photos = Column(String)
    popular_reviews = Column(String)
    playable = Column(Boolean)
    tag = Column(String)
    sort = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'movie',
    }
