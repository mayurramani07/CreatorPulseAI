from app.services.cache_service import (
    cache_analysis,
    delete_cached_analysis,
    get_cached_analysis,
)


video_id = "test_video_123"

test_data = {
    "processed_comments": 10,
    "content_request_candidates": 3,
    "topic_groups": 2,
    "recommendations": [
        {
            "topic": "Agentic AI",
            "demand_score": 0.85,
        }
    ],
}


cache_analysis(
    video_id,
    test_data,
)

cached_data = get_cached_analysis(
    video_id
)

print("Cached data:")
print(cached_data)

delete_cached_analysis(
    video_id
)

deleted_data = get_cached_analysis(
    video_id
)

print("After delete:")
print(deleted_data)