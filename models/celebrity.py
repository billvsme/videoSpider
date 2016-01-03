from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Datetime
from .base import Base


class Celebrity(Base):
    __tablename__ = 'celebrities'

    id = Column(Integer, primary_key=True)
    douban_id = Column(String)
    name = Column(String)
    name_en = Column(String)
    alt = Column(String)
    mobile_url = Column(String)
    avatars = Column(String)
    summary = Column(String)
    aka = Column(String)
    aka_en = Column(String)
    website = Column(String)
    gender = Column(String)
    birthday = Column(String)
    born_place = Column(String)
    professions = Column(String)
    constellation = Column(String)
    photos = Column(String)
    rks = Column(String)
