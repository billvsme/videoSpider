# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from models import Base


class AnimationGenre(Base):
    __tablename__ = 'animation_genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
