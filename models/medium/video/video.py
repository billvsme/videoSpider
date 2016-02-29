# -*- coding: utf-8 -*-
from sqlalchemy import (Column, Integer, BigInteger, String, Boolean, DateTime,
                        ForeignKey)
from sqlalchemy.orm import relationship
from models import Base
from ..medium import Medium


class Video(Medium):
    __tablename__ = 'videos'

    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    subtype = Column(String)
    official_site = Column(String)
    total_count = Column(Integer)
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

    __mapper_args__ = {
        'polymorphic_identity': 'video',
    }
