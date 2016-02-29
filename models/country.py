# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from .base import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
