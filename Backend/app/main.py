from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Analysis, Recommendation, Video

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


app = FastAPI(
    title="CreatorPulse AI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


@app.get("/videos/{video_id}")
async def read_video(
    video_id: str,
):
    return get_video(
        video_id
    )


@app.get("/videos/{video_id}/comments")
def get_video_comments(
    video_id: str,
):
    return get_comments(
        video_id
    )


@app.get(
    "/videos/{video_id}/sample-comments"
)
def get_sample_comments(
    video_id: str,
    db: Session = Depends(get_db),
):
    try:
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

        sampled_comments = build_sample(
            comments,
            sample_size=min(
                collection_limit,
                len(comments),
            ),
        )

        processed_comments = preprocess_comments(
            sampled_comments
        )

        request_comments = detect_content_requests(
            processed_comments
        )

        topic_groups = group_request_comments(
            request_comments
        )

        recommendations = build_topic_recommendations(
            topic_groups
        )

        video_response = get_video(
            video_id
        )

        video_item = (
            video_response
            .get("items", [{}])[0]
        )

        snippet = video_item.get(
            "snippet",
            {}
        )

        statistics = video_item.get(
            "statistics",
            {}
        )

        db_video = (
            db.query(Video)
            .filter(
                Video.youtube_video_id == video_id
            )
            .first()
        )

        if db_video is None:
            db_video = Video(
                youtube_video_id=video_id,
                title=snippet.get(
                    "title",
                    "YouTube Video",
                ),
                channel_name=snippet.get(
                    "channelTitle",
                    "",
                ),
                thumbnail_url=(
                    snippet
                    .get("thumbnails", {})
                    .get("high", {})
                    .get("url", "")
                ),
                view_count=int(
                    statistics.get(
                        "viewCount",
                        0,
                    )
                ),
                like_count=int(
                    statistics.get(
                        "likeCount",
                        0,
                    )
                ),
                comment_count=int(
                    statistics.get(
                        "commentCount",
                        total_comments,
                    )
                ),
            )

            db.add(db_video)

        else:
            db_video.title = snippet.get(
                "title",
                db_video.title,
            )

            db_video.channel_name = snippet.get(
                "channelTitle",
                db_video.channel_name,
            )

            db_video.thumbnail_url = (
                snippet
                .get("thumbnails", {})
                .get("high", {})
                .get(
                    "url",
                    db_video.thumbnail_url,
                )
            )

            db_video.view_count = int(
                statistics.get(
                    "viewCount",
                    db_video.view_count,
                )
            )

            db_video.like_count = int(
                statistics.get(
                    "likeCount",
                    db_video.like_count,
                )
            )

            db_video.comment_count = int(
                statistics.get(
                    "commentCount",
                    total_comments,
                )
            )

        db.flush()

        db_analysis = Analysis(
            video_id=db_video.id,
            processed_comments=len(
                processed_comments
            ),
            content_request_candidates=len(
                request_comments
            ),
            topic_groups=len(
                topic_groups
            ),
        )

        db.add(db_analysis)

        db.flush()

        for recommendation in recommendations:
            db_recommendation = Recommendation(
                analysis_id=db_analysis.id,
                topic=recommendation.get(
                    "topic",
                    "Untitled Topic",
                ),
                demand_score=float(
                    recommendation.get(
                        "demand_score",
                        0,
                    )
                ),
                request_count=int(
                    recommendation.get(
                        "request_count",
                        0,
                    )
                ),
                total_likes=int(
                    recommendation.get(
                        "total_likes",
                        0,
                    )
                ),
                total_replies=int(
                    recommendation.get(
                        "total_replies",
                        0,
                    )
                ),
                representative_comment=(
                    recommendation.get(
                        "representative_comment",
                        "",
                    )
                ),
            )

            db.add(db_recommendation)

        db.commit()

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
        db.rollback()

        print(
            f"Error analyzing video "
            f"{video_id}: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


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