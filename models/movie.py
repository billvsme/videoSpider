from sqlalchemy import Table
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .subject import Subject


movie_genre_table = Table('movies_genres_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('movie_genre_id', Integer, ForeignKey('movie_genres.id'))
)

movie_country_table = Table('movies_countries_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('movie_country_id', Integer, ForeignKey('movie_countries.id'))
)

movie_language_table = Table('movies_languages_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('movie_language_id', Integer, ForeignKey('movie_languages.id'))
)


class Movie(Subject):
    __tablename__ = 'movies'

    id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
    subtype = Column(String)
    official_site = Column(String)
    imdb_number = Column(String)
    duration = Column(String)
    year = Column(String)
    current_season = Column(Integer)
    photos = Column(String)
    thumbnail_photos = Column(String)
    wallpapers = Column(String)
    thumbnail_wallpapers = Column(String)
    playable = Column(Boolean)

    crawler_tag = Column(String)
    crawler_sort = Column(String)

    languages = relationship('MovieLanguage',
            secondary=movie_language_table,
            backref='movies'
    )
    genres = relationship('MovieGenre',
            secondary=movie_genre_table,
            backref='movies'
    )
    countries = relationship('MovieCountry',
            secondary=movie_country_table,
            backref='movies'
    )

    __mapper_args__ = {
        'polymorphic_identity': 'movie',
    }


class MovieGenre(Base):
    __tablename__ = 'movie_genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class MovieCountry(Base):
    __tablename__ = 'movie_countries'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class MovieLanguage(Base):
    __tablename__ = 'movie_languages'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
