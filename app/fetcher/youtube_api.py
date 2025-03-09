import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import time
from config.settings import SEARCH_QUERY

logger = logging.getLogger(__name__)

class YouTubeAPIError(Exception):
    pass

# Class to interact with the YouTube API
class YouTubeAPI:
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.quota_exceeded = False
        self.retry_after = 0

    def fetch_latest_videos(self, query: str = SEARCH_QUERY, max_results: int = 10) -> Optional[Dict]:
        """
        Fetch latest videos from YouTube with error handling and retries
        """
        # Check if the quota is exceeded and if the retry time has not passed
        if self.quota_exceeded:
            if time.time() < self.retry_after:
                logger.warning("API quota still exceeded, waiting...")
                return None
            self.quota_exceeded = False

        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'order': 'date',
            'maxResults': max_results,
            'key': self.api_key
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            
            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 403:
                error_message = response.json().get('error', {}).get('message', '')
                if 'quota' in error_message.lower():
                    self.quota_exceeded = True
                    self.retry_after = time.time() + 3600  # Wait for 1 hour
                    logger.error("YouTube API quota exceeded. Waiting for 1 hour.")
                else:
                    logger.error(f"API key authentication error: {error_message}")
                return None
            
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 300))
                self.retry_after = time.time() + retry_after
                logger.warning(f"Rate limit exceeded. Waiting for {retry_after} seconds.")
                return None
            
            else:
                logger.error(f"YouTube API error: Status {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return None

# Class to manage multiple API keys for the YouTube API
class YouTubeAPIManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.current_key_index = 0
        self.apis = [YouTubeAPI(key) for key in api_keys]

    def get_current_api(self):
        return self.apis[self.current_key_index]

    def rotate_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.apis)
        logger.info(f"Rotating to API key {self.current_key_index + 1}")

    async def fetch_videos(self, query=SEARCH_QUERY, max_results=10):
        attempts = 0
        max_attempts = len(self.apis)

        while attempts < max_attempts:
            api = self.get_current_api()
            result = api.fetch_latest_videos(query, max_results)

            if result is not None:
                return result

            self.rotate_api_key()
            attempts += 1

        logger.error("All API keys exhausted or encountered errors")
        return None