# YouTube Video Fetcher  

This project is a **YouTube Video Fetcher** that uses the YouTube Data API to fetch and store metadata for videos related to a specific search query. The fetched videos are saved into a database for further usage.  

## Flow Diagram

![image](https://github.com/user-attachments/assets/053e77c1-a1a9-4dd7-ab7b-73448be5da5d)


## Features  

- Fetch YouTube videos based on a search query.  
- Store video metadata in a relational database.  
- API endpoints for fetching and searching videos.  
- Handles API quota limits and rotates multiple API keys.  
- Scheduler to periodically fetch new videos.  
- Integrated logging for debugging and monitoring.  

## Technologies Used  

- **Backend Framework**: FastAPI  
- **Database**: SQLAlchemy with PostgreSQL  
- **Scheduler**: APScheduler  
- **YouTube Data API v3**  
- **Logging**: Python’s `logging` module  

## Prerequisites  

Ensure you have the following installed:  
- Python 3.8+  
- A YouTube Data API key (or multiple keys) [(reference)](https://developers.google.com/youtube/v3/quickstart/python)
- Docker and Docker Compose  
 

## Setup  and Execution

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/v-v-sumanth-kumar/Youtube_API.git
   cd Youtube_API
2. **Execute the below command**

    docker-compose up --build

## Sample Requests and Response

1. **/Videos/Search**
    ![image](https://github.com/user-attachments/assets/f7729ae3-eda3-4e29-8514-8dd3d224212d)

2. **/Videos**
    ![image](https://github.com/user-attachments/assets/d126f521-d3ed-48c7-8613-15e3a2d2c4fd)

