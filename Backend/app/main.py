from fastapi import FastAPI
from app.services.youtube_service import get_video
from app.services.youtube_service import get_comments
app = FastAPI(title="CreatorPulse AI")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/videos/{video_id}")
async def read_video(video_id: str):
    return get_video(video_id)

@app.get("/videos/{video_id}/comments")
def get_video_comments(video_id: str):
    return get_comments(video_id)