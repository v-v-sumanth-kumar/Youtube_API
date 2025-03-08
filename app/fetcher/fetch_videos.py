import asyncio
import os
import sys
from datetime import datetime
import json
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from app.fetcher.youtube_api import fetch_latest_videos
from app.models.database import SessionLocal, Base, engine
from app.models.video import Video

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

async def save_videos():
    while True:
        db = SessionLocal()
        try:
            logger.info("Fetching latest videos...")
            data = fetch_latest_videos()
            
            videos_added = 0
            videos_updated = 0
            
            for item in data.get("items", []):
                try:
                    video_id = item["id"]["videoId"]
                    snippet = item["snippet"]
                    
                    # Convert published_at string to datetime
                    published_at = datetime.strptime(
                        snippet["publishedAt"],
                        "%Y-%m-%dT%H:%M:%SZ"
                    )
                    
                    # Prepare video data
                    video_data = {
                        "id": video_id,
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "published_at": published_at,
                        "thumbnails": json.dumps(snippet["thumbnails"]),
                        "channel_title": snippet.get("channelTitle")
                    }
                    
                    # Using PostgreSQL's UPSERT functionality
                    stmt = insert(Video).values(video_data)
                    stmt = stmt.on_conflict_do_update(
                        index_elements=['id'],
                        set_=video_data
                    )
                    
                    result = db.execute(stmt)
                    db.commit()
                    
                    if result.rowcount > 0:
                        videos_added += 1
                    
                except SQLAlchemyError as e:
                    logger.error(f"Database error processing video {video_id}: {e}")
                    db.rollback()
                except Exception as e:
                    logger.error(f"Error processing video {video_id}: {e}")
                    continue
            
            logger.info(f"Added/Updated {videos_added} videos in database")
            
            await asyncio.sleep(10)  # Fetch every 10 seconds
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await asyncio.sleep(30)  # Wait longer on error
        finally:
            db.close()

async def main():
    try:
        await save_videos()
    except KeyboardInterrupt:
        logger.info("Stopping the video fetcher...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())