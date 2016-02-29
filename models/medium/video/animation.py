# -*- coding: utf-8 -*-
from sqlalchemy import Table
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
from .video import Video

animation_genre_table = Table(
    'animations_genres_association',
    Base.metadata,
    Column('animation_id', Integer, ForeignKey('animations.id')),
    Column('animation_genre_id', Integer, ForeignKey('animation_genres.id'))
)


class Animation(Video):
    __tablename__ = 'animations'
    id = Column(Integer, ForeignKey('videos.id'), primary_key=True)

    genres = relationship(
        'AnimationGenre',
        secondary=animation_genre_table,
        backref='animations'
    )

    __mapper_args__ = {
        'polymorphic_identity': 'animation',
    }
