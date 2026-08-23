import redis


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    protocol=2,
)


def test_redis_connection():
    try:
        redis_client.ping()
        print("Redis connection successful.")
    except redis.RedisError as exc:
        print(
            f"Redis connection failed: {exc}"
        )