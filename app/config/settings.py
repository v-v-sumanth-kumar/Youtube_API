import os
from dotenv import load_dotenv

load_dotenv()

# List of YouTube API keys loaded from the environment
YOUTUBE_API_KEYS = [
    os.getenv("YOUTUBE_API_KEY_1"),
    os.getenv("YOUTUBE_API_KEY_2"),
    os.getenv("YOUTUBE_API_KEY_3"),
]

SEARCH_QUERY = "cricket"  # Default search term for fetching videos from YouTube
MAX_RESULTS = 10
FETCH_INTERVAL = 10

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
