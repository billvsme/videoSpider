# -*- coding: utf-8 -*-
from sqlalchemy import Table
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
from .video import Video

tv_genre_table = Table(
    'tvs_genres_association',
    Base.metadata,
    Column('tv_id', Integer, ForeignKey('tvs.id')),
    Column('tv_genre_id', Integer, ForeignKey('tv_genres.id'))
)


class TV(Video):
    __tablename__ = 'tvs'
    id = Column(Integer, ForeignKey('videos.id'), primary_key=True)

    genres = relationship(
        'TVGenre',
        secondary=tv_genre_table,
        backref='tvs'
    )

    __mapper_args__ = {
        'polymorphic_identity': 'tv',
    }
