from sqlalchemy import Column, String, Text, DateTime, JSON
from app.models.database import Base
import datetime

class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime, index=True, nullable=False)
    thumbnails = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    channel_title = Column(String(255), nullable=True)


class csds(Base):
    __tablename__ = "vicdsdeos"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime, index=True, nullable=False)
    thumbnails = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)