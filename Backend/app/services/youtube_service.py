from googleapiclient.discovery import build

from app.config import YOUTUBE_API_KEY


youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY,
)

def get_video(video_id: str):
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id,
    ).execute()

    return response

def get_comments(video_id: str, max_results: int = 100):
    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText",
    ).execute()

    return response