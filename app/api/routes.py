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


@router.post("/videos")
def create_video(video: VideoCreate, db: Session = Depends(get_db)):
    # Convert published_at to a datetime object
    try:
        published_at_dt = datetime.fromisoformat(video.published_at)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format for published_at")

    # Create a unique ID for the video
    video_id = str(uuid.uuid4())

    # Check if a video with the same published_at and title already exists
    existing_video = (
        db.query(Video)
        .filter(Video.title == video.title, Video.published_at == published_at_dt)
        .first()
    )
    if existing_video:
        raise HTTPException(status_code=400, detail="Video already exists")

    # Create a new video instance
    new_video = Video(
        id=video_id,
        title=video.title,
        description=video.description,
        published_at=published_at_dt,
        thumbnails=video.thumbnails,
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return {"message": "Video created successfully", "video": new_video}
