from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.video import Video
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/videos")
def get_videos(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    videos = db.query(Video).order_by(Video.published_at.desc()).offset(offset).limit(page_size).all()
    return videos

@router.get("/videos/search")
def search_videos(query: str, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    videos = db.query(Video).filter(Video.title.ilike(f"%{query}%") | Video.description.ilike(f"%{query}%")).order_by(Video.published_at.desc()).offset(offset).limit(page_size).all()
    return videos


# Define a schema for the video input
class VideoCreate(BaseModel):
    title: str
    description: str
    published_at: str  # Expecting ISO 8601 formatted datetime string
    thumbnails: dict
