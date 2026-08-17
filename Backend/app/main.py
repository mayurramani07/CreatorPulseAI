from fastapi import FastAPI
from app.services.youtube_service import get_video
from app.services.youtube_service import get_comments
from app.services.sampling_service import build_sample
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

@app.get("/videos/{video_id}/sample-comments")
def get_sample_comments(video_id: str):

    comments = get_comments(
        video_id,
        max_comments=500,
    )

    sampled_comments = build_sample(
        comments,
        sample_size=300,
    )

    return {
        "total_collected": len(comments),
        "sample_size": len(sampled_comments),
        "comments": sampled_comments,
    }