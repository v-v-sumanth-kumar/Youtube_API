import requests
import os

API_KEY = "AIzaSyBE03Zf47jVxnjeuP_gIOrHlE2nZ4mPlOw"
SEARCH_QUERY = "Python Programming"
BASE_URL = "https://www.googleapis.com/youtube/v3/search"

def fetch_latest_videos():
    params = {
        "part": "snippet",
        "q": SEARCH_QUERY,
        "type": "video",
        "order": "date",
        "maxResults": 10,
        "key": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()
