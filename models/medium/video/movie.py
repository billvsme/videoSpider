# -*- coding: utf-8 -*-
from sqlalchemy import Table
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
from .video import Video

movie_genre_table = Table(
    'movies_genres_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('movie_genre_id', Integer, ForeignKey('movie_genres.id'))
)


class Movie(Video):
    __tablename__ = 'movies'
    id = Column(Integer, ForeignKey('videos.id'), primary_key=True)

    genres = relationship(
        'MovieGenre',
        secondary=movie_genre_table,
        backref='movies'
    )

    __mapper_args__ = {
        'polymorphic_identity': 'movie',
    }
