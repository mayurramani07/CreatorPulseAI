import os
import redis
from dotenv import load_dotenv
load_dotenv()

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)
redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
    protocol=2,
)
def test_redis_connection():
    try:
        redis_client.ping()
        print(
            "Redis connection successful."
        )
    except redis.RedisError as exc:
        print(
            f"Redis connection failed: {exc}"
        )