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


def run_analysis(video_id: str):
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

    return {
        "total_available": total_comments,
        "total_collected": len(comments),
        "sample_size": len(sampled_comments),
        "processed_comments": len(processed_comments),
        "content_request_candidates": len(request_comments),
        "topic_groups": len(topic_groups),
        "recommendations": recommendations,
    }

