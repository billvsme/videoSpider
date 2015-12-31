from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, func
from sqlalchemy.dialects import postgresql, mysql, sqlite
from .base import Base


class Subject(Base):
    __tablename__ = 'subjects'

    #id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    #id = Column(BigInteger, primary_key=True)
    id = Column(Integer, primary_key=True)
    douban_id = Column(String)
    title = Column(String)
    cover = Column(String)
    cover_x = Column(Integer)
    cover_y = Column(Integer)
    playable = Column(Boolean)
    is_new = Column(Boolean)
    is_beetle_subject = Column(Boolean)
    rate = Column(String)
    douban_url = Column(String)
    type_ = Column(String)
    tag = Column(String)
    sort = Column(String)

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
