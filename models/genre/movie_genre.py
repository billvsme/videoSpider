# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from models import Base


class MovieGenre(Base):
    __tablename__ = 'movie_genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
