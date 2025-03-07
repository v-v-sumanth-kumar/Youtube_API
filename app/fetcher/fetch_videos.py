import asyncio
from app.fetcher.youtube_api import fetch_latest_videos
from app.models.database import SessionLocal, Base, engine
from app.models.video import Video

Base.metadata.create_all(bind=engine)

async def save_videos():
    db = SessionLocal()
    while True:
        data = fetch_latest_videos()
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            video = db.query(Video).filter_by(id=video_id).first()
            if not video:
                new_video = Video(
                    id=video_id,
                    title=snippet["title"],
                    description=snippet["description"],
                    published_at=snippet["publishedAt"],
                    thumbnails=snippet["thumbnails"],
                )
                db.add(new_video)
        db.commit()
        await asyncio.sleep(10)  # Fetch every 10 seconds

if __name__ == "__main__":
    asyncio.run(save_videos())
