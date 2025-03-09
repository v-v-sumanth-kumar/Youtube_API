from math import ceil
from operator import or_, and_
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import true
from models.database import get_db
from models.video import Video

router = APIRouter()

@router.get("/videos")
def get_videos(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    """
    Fetch a paginated list of videos, sorted by the publication date in descending order.
    """
    offset = (page - 1) * page_size
    videos = db.query(Video).order_by(Video.published_at.desc()).offset(offset).limit(page_size).all()
    return videos

@router.get("/videos/search")
def search_videos(query: str, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    """
    Search videos by matching query terms in the title or description, with pagination.
    """
    query_terms = query.split()
    title_filters = [Video.title.ilike(f"%{term}%") for term in query_terms] # Generate filters for title based on the query terms
    if title_filters:
        # Combine multiple filters with AND logic
        title_filter = and_(*title_filters) if len(title_filters) > 1 else title_filters[0]
    else:
        # If no query terms, use a filter that always evaluates to true
        title_filter = true()  
    description_filters = [Video.description.ilike(f"%{term}%") for term in query_terms] # Generate filters for description based on the query terms
    if description_filters:
        # Combine multiple filters with AND logic
        description_filter = and_(*description_filters) if len(description_filters) > 1 else description_filters[0]
    else:
        # If no query terms, use a filter that always evaluates to true
        description_filter = true()
    combined_filter = or_(title_filter, description_filter) # Combine title and description filters using OR logic
    offset = (page - 1) * page_size

    # Query the videos from the database using the combined filter
    videos = (
        db.query(Video)
        .filter(combined_filter)
        .order_by(Video.published_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return videos