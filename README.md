# YouTube Video Fetcher  

This project is a **YouTube Video Fetcher** that uses the YouTube Data API to fetch and store metadata for videos related to a specific search query. The fetched videos are saved into a database for further usage.  

## Features  

- Fetch YouTube videos based on a search query.  
- Store video metadata in a relational database.  
- API endpoints for fetching and searching videos.  
- Handles API quota limits and rotates multiple API keys.  
- Scheduler to periodically fetch new videos.  
- Integrated logging for debugging and monitoring.  

## Technologies Used  

- **Backend Framework**: FastAPI  
- **Database**: SQLAlchemy with SQLite or PostgreSQL (via `DATABASE_URL`)  
- **Scheduler**: APScheduler  
- **YouTube Data API v3**  
- **Logging**: Python’s `logging` module  

## Prerequisites  

Ensure you have the following installed:  
- Python 3.8+  
- A YouTube Data API key (or multiple keys) [(reference)](https://developers.google.com/youtube/v3/quickstart/python)
- Docker and Docker Compose  
 

## Setup  

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/v-v-sumanth-kumar/Youtube_API.git
   cd Youtube_API
