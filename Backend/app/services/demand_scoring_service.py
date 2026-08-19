def normalize(
    value: float,
    maximum: float,
) -> float:
    """
    Normalize a value between 0 and 1.
    """

    if maximum <= 0:
        return 0.0

    return value / maximum


def calculate_topic_demand(
    topic_comments: list[dict],
    max_request_count: int,
    max_likes: int,
    max_replies: int,
) -> dict:
    """
    Calculate normalized demand signals for a topic.

    Signals:
    - request frequency
    - total likes
    - total replies

    Final weighting:
    - 50% request frequency
    - 35% likes
    - 15% replies
    """

    if not topic_comments:
        return {
            "request_count": 0,
            "total_likes": 0,
            "total_replies": 0,
            "request_score": 0.0,
            "like_score": 0.0,
            "reply_score": 0.0,
            "demand_score": 0.0,
        }

    request_count = len(topic_comments)

    total_likes = sum(
        comment.get("like_count", 0)
        for comment in topic_comments
    )

    total_replies = sum(
        comment.get("reply_count", 0)
        for comment in topic_comments
    )

    request_score = normalize(
        request_count,
        max_request_count,
    )

    like_score = normalize(
        total_likes,
        max_likes,
    )

    reply_score = normalize(
        total_replies,
        max_replies,
    )

    demand_score = (
        request_score * 0.50
        + like_score * 0.35
        + reply_score * 0.15
    )

    return {
        "request_count": request_count,
        "total_likes": total_likes,
        "total_replies": total_replies,
        "request_score": round(request_score, 4),
        "like_score": round(like_score, 4),
        "reply_score": round(reply_score, 4),
        "demand_score": round(demand_score, 4),
    }