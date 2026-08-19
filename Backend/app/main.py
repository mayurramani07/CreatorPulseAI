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

from app.services.preprocessing_service import (
    preprocess_comments,
)

from app.services.request_detector import (
    detect_content_requests,
)

from app.services.topic_grouping_service import (
    group_similar_comments,
)

from app.services.recommendation_service import (
    build_topic_recommendations,
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
  

    total_comments = get_comment_count(
        video_id
    )


    collection_limit = determine_sample_size(
        total_comments
    )

    comments = get_comments(
        video_id,
        max_comments=collection_limit,
    )

    sampled_comments = build_sample(
        comments,
        sample_size=collection_limit,
    )

    processed_comments = preprocess_comments(
        sampled_comments
    )


    request_comments = detect_content_requests(
        processed_comments
    )


    topic_groups = group_similar_comments(
        request_comments
    )


    recommendations = build_topic_recommendations(
        topic_groups
    )


    return {
        "total_available": total_comments,
        "total_collected": len(comments),
        "sample_size": len(sampled_comments),
        "processed_comments": len(processed_comments),
        "content_request_candidates": len(
            request_comments
        ),
        "topic_groups": len(topic_groups),
        "recommendations": recommendations,
    }


@app.get("/videos/{video_id}/comment-count")
def comment_count(video_id: str):

    return {
        "video_id": video_id,
        "total_comments": get_comment_count(
            video_id
        ),
    }