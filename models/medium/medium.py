# -*- coding: utf-8 -*-
from sqlalchemy import Table
from sqlalchemy import (Column, Integer, BigInteger, String, Boolean,
                        DateTime, func, ForeignKey)
from sqlalchemy.dialects import postgresql, mysql, sqlite
from sqlalchemy.orm import relationship
from models import Base


medium_country_table = Table(
    'media_countries_association',
    Base.metadata,
    Column('medium_id', Integer, ForeignKey('media.id')),
    Column('medium_country_id', Integer, ForeignKey('countries.id'))
)

medium_language_table = Table(
    'media_languages_association',
    Base.metadata,
    Column('medium_id', Integer, ForeignKey('media.id')),
    Column('medium_language_id', Integer, ForeignKey('languages.id'))
)


class Medium(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    aliases = Column(String)
    summary = Column(String)
    cover = Column(String)
    covers = Column(String)
    thumbnail_covers = Column(String)
    pubdate = Column(String)

    is_detail = Column(Boolean, default=False)

    douban_id = Column(String)
    douban_url = Column(String)
    cover_x = Column(Integer)
    cover_y = Column(Integer)
    is_new = Column(Boolean)
    is_beetle_subject = Column(Boolean)
    douban_rate = Column(String)
    douban_rating = Column(String)
    douban_ratings_count = Column(String)

    bilibili_id = Column(String)

    languages = relationship(
            'Language',
            secondary=medium_language_table,
            backref='media'
    )
    countries = relationship(
            'Country',
            secondary=medium_country_table,
            backref='media'
    )

    type = Column(String(50))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    __mapper_args__ = {
        'polymorphic_identity': 'medium',
        'polymorphic_on': type
    }
