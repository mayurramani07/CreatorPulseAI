from fastapi import FastAPI

from app.services.youtube_service import (
    get_video,
    get_comments,
    get_comment_count,
)

from app.services.sampling_service import (
    build_sample,
    determine_sample_size,
)


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
    total_comments = get_comment_count(video_id)
    collection_limit = determine_sample_size(total_comments)
    comments = get_comments(
        video_id,
        max_comments=collection_limit,
    )
    sampled_comments = build_sample(
        comments,
        sample_size=collection_limit,
    )
    return {
        "total_available": total_comments,
        "total_collected": len(comments),
        "sample_size": len(sampled_comments),
        "comments": sampled_comments,
    }

@app.get("/videos/{video_id}/comment-count")
def comment_count(video_id: str):

    return {
        "video_id": video_id,
        "total_comments": get_comment_count(video_id),
    }