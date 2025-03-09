from fastapi import FastAPI
from api.routes import router
from models.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fetcher.fetch_videos import save_videos


app = FastAPI()

# Event handler for application startup
@app.on_event("startup")
async def startup_event():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(save_videos, IntervalTrigger(seconds=10))  # Schedule the `save_videos` function to run every 10 seconds
    scheduler.start()
    app.state.scheduler = scheduler  # Store the scheduler in the app state
    print("Scheduler started")

# Event handler for application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    scheduler = app.state.scheduler
    if scheduler:
        scheduler.shutdown()
    print("Scheduler shut down")

# Event handler for application shutdown
Base.metadata.create_all(bind=engine)

# Include the router for API endpoints
app.include_router(router)

