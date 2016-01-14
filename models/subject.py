from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, func
from sqlalchemy.dialects import postgresql, mysql, sqlite
from .base import Base


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    douban_id = Column(String)
    douban_url = Column(String)
    title = Column(String)
    aliases = Column(String)
    cover = Column(String)
    cover_x = Column(Integer)
    cover_y = Column(Integer)
    is_new = Column(Boolean)
    is_beetle_subject = Column(Boolean)
    douban_rate = Column(String)
    douban_rating = Column(String)
    douban_ratings_count = Column(String)
    summary = Column(String)
    pubdate = Column(String)

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
        'polymorphic_identity':'subject',
        'polymorphic_on': type
    }
