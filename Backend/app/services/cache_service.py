import json

from app.redis_client import redis_client


CACHE_TTL = 60 * 60
CACHE_VERSION = "v1"


def _cache_key(video_id: str) -> str:
    return f"analysis:{CACHE_VERSION}:{video_id}"


def get_cached_analysis(video_id: str):
    key = _cache_key(video_id)

    cached_data = redis_client.get(key)

    if not cached_data:
        return None

    return json.loads(cached_data)


def cache_analysis(
    video_id: str,
    analysis: dict,
):
    key = _cache_key(video_id)

    redis_client.setex(
        key,
        CACHE_TTL,
        json.dumps(
            analysis,
            ensure_ascii=False,
        ),
    )


def delete_cached_analysis(
    video_id: str,
):
    key = _cache_key(video_id)

    redis_client.delete(key)