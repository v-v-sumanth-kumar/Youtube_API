import asyncio
import os
import sys
from datetime import datetime
import logging
from sqlalchemy.exc import SQLAlchemyError

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from app.fetcher.youtube_api import YouTubeAPIManager
from app.models.database import SessionLocal
from app.models.video import Video
from app.config.settings import YOUTUBE_API_KEYS, FETCH_INTERVAL

# Set up logger for the YouTube fetcher
logger = logging.getLogger("youtube_fetcher")
logger.setLevel(logging.INFO)

# Console handler for logging to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler for logging to a file
file_handler = logging.FileHandler('logs/youtube_fetcher.log')
file_handler.setLevel(logging.INFO)

# Formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Async function to fetch and save YouTube videos to the database
async def save_videos():
    """
    Fetch the latest videos from the YouTube API and save them to the database.
    Uses multiple API keys for load balancing and handles retries on failure.
    """
    api_manager = YouTubeAPIManager(YOUTUBE_API_KEYS)
    db = SessionLocal()
    
    try:
        while True:
            logger.info("Fetching latest videos...")
            data = await api_manager.fetch_videos()
            
            if data is None:
                logger.warning("No data received, waiting before next attempt...")
                await asyncio.sleep(FETCH_INTERVAL)
                continue

            videos_added = 0
            for item in data.get("items", []):
                try:
                    video_id = item["id"]["videoId"]
                    snippet = item["snippet"]
                    
                    video = db.query(Video).filter_by(id=video_id).first()
                    
                    if not video:
                        published_at = datetime.strptime(
                            snippet["publishedAt"],
                            "%Y-%m-%dT%H:%M:%SZ"
                        )
                        
                        new_video = Video(
                            id=video_id,
                            title=snippet["title"],
                            description=snippet["description"],
                            published_at=published_at,
                            thumbnails=snippet["thumbnails"],
                            channel_title=snippet.get("channel_title", "")
                        )
                        
                        db.add(new_video)
                        videos_added += 1
                        logger.info(f"Adding new video: {video_id}")
                
                except Exception as e:
                    logger.error(f"Error processing video {video_id}: {e}")
                    continue
            
            if videos_added > 0:
                db.commit()
                logger.info(f"Added {videos_added} new videos to database")
            
            await asyncio.sleep(FETCH_INTERVAL)
            
    except Exception as e:
        logger.error(f"An error occurred: {e} {YOUTUBE_API_KEYS}")
    finally:
        db.close()