# -*- coding: utf-8 -*-
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, BigInteger, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base


medium_director_table = Table(
    'media_directors_association',
    Base.metadata,
    Column('medium_id', Integer, ForeignKey('media.id')),
    Column('celebrity_id', Integer, ForeignKey('celebrities.id'))
)

medium_playwright_table = Table(
    'media_playwrights_association',
    Base.metadata,
    Column('medium_id', Integer, ForeignKey('media.id')),
    Column('celebrity_id', Integer, ForeignKey('celebrities.id'))
)

medium_actor_table = Table(
    'media_actors_association',
    Base.metadata,
    Column('medium_id', Integer, ForeignKey('media.id')),
    Column('celebrity_id', Integer, ForeignKey('celebrities.id'))
)


class Celebrity(Base):
    __tablename__ = 'celebrities'

    id = Column(Integer, primary_key=True)
    douban_id = Column(String, unique=True)
    douban_url = Column(String)
    name = Column(String)
    name_en = Column(String)
    aliases = Column(String)
    aliases_en = Column(String)
    sex = Column(String)
    cover = Column(String)
    thumbnail_cover = Column(String)
    website = Column(String)
    gender = Column(String)
    birthday = Column(String)
    born_place = Column(String)
    family = Column(String)
    professions = Column(String)
    constellation = Column(String)
    photos = Column(String)
    thumbnail_photos = Column(String)
    imdb_number = Column(String)
    summary = Column(String)

    is_detail = Column(Boolean, default=False)

    director_media = relationship(
        "Medium",
        secondary=medium_director_table,
        backref='directors'
    )

    playwright_media = relationship(
        "Medium",
        secondary=medium_playwright_table,
        backref='playwrights'
    )

    actor_media = relationship(
        "Medium",
        secondary=medium_actor_table,
        backref='actors'
    )
