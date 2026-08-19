from fastapi import FastAPI, HTTPException

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

from app.services.llm_topic_service import (
    group_request_comments,
)

from app.services.recommendation_service import (
    build_topic_recommendations,
)


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="CreatorPulse AI"
)


# =========================================================
# Health Check
# =========================================================

@app.get("/health")
async def health_check():

    return {
        "status": "healthy"
    }


# =========================================================
# Get Video
# =========================================================

@app.get("/videos/{video_id}")
async def read_video(
    video_id: str,
):

    return get_video(
        video_id
    )


# =========================================================
# Get All Comments
# =========================================================

@app.get("/videos/{video_id}/comments")
def get_video_comments(
    video_id: str,
):

    return get_comments(
        video_id
    )


# =========================================================
# Analyze Comments
# =========================================================

@app.get(
    "/videos/{video_id}/sample-comments"
)
def get_sample_comments(
    video_id: str,
):

    try:

        # -------------------------------------------------
        # 1. Get total comment count
        # -------------------------------------------------

        total_comments = get_comment_count(
            video_id
        )

        # -------------------------------------------------
        # 2. Determine collection size
        # -------------------------------------------------

        collection_limit = (
            determine_sample_size(
                total_comments
            )
        )

        # -------------------------------------------------
        # 3. Collect comments from YouTube
        # -------------------------------------------------

        comments = get_comments(
            video_id,
            max_comments=collection_limit,
        )

        if not comments:

            return {
                "total_available": total_comments,
                "total_collected": 0,
                "sample_size": 0,
                "processed_comments": 0,
                "content_request_candidates": 0,
                "topic_groups": 0,
                "recommendations": [],
            }

        # -------------------------------------------------
        # 4. Build sample
        # -------------------------------------------------

        sampled_comments = build_sample(
            comments,
            sample_size=min(
                collection_limit,
                len(comments),
            ),
        )

        # -------------------------------------------------
        # 5. Preprocess comments
        # -------------------------------------------------

        processed_comments = (
            preprocess_comments(
                sampled_comments
            )
        )

        # -------------------------------------------------
        # 6. Detect content requests
        #
        # Embedding model handles semantic
        # request detection.
        # -------------------------------------------------

        request_comments = (
            detect_content_requests(
                processed_comments
            )
        )

        # -------------------------------------------------
        # 7. Semantic topic grouping
        #
        # GPT-OSS-20B handles:
        #
        #   comments
        #       ↓
        #   semantic understanding
        #       ↓
        #   topic grouping
        #       ↓
        #   topic names
        #
        # One LLM call.
        # -------------------------------------------------

        topic_groups = (
            group_request_comments(
                request_comments
            )
        )

        # -------------------------------------------------
        # 8. Demand scoring
        #
        # Pure Python.
        #
        # No additional LLM call.
        # -------------------------------------------------

        recommendations = (
            build_topic_recommendations(
                topic_groups
            )
        )

        # -------------------------------------------------
        # 9. Final response
        # -------------------------------------------------

        return {
            "total_available": total_comments,

            "total_collected": len(
                comments
            ),

            "sample_size": len(
                sampled_comments
            ),

            "processed_comments": len(
                processed_comments
            ),

            "content_request_candidates": len(
                request_comments
            ),

            "topic_groups": len(
                topic_groups
            ),

            "recommendations": recommendations,
        }

    except Exception as exc:

        print(
            f"Error analyzing video "
            f"{video_id}: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# =========================================================
# Comment Count
# =========================================================

@app.get(
    "/videos/{video_id}/comment-count"
)
def comment_count(
    video_id: str,
):

    return {
        "video_id": video_id,

        "total_comments": (
            get_comment_count(
                video_id
            )
        ),
    }