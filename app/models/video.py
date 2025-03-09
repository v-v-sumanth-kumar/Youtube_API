from sqlalchemy import Column, String, Text, DateTime, JSON
from models.database import Base
import datetime

class Video(Base):
    """
    Video model representing the 'videos' table in the database.
    """
    __tablename__ = "videos"
    __table_args__ = {'extend_existing': True}  # Allows updating existing table definitions if needed
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime, index=True, nullable=False)
    thumbnails = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    channel_title = Column(String(255), nullable=True)
    
