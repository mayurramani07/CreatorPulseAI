def calculate_topic_demand(topic_comments: list[dict]) -> dict:
    """
    Calculate demand signals for a topic.

    Signals:
    - number of comments requesting the topic
    - total likes
    - total replies
    """

    if not topic_comments:
        return {
            "request_count": 0,
            "total_likes": 0,
            "total_replies": 0,
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

    demand_score = (
        request_count * 1.0
        + total_likes * 0.5
        + total_replies * 0.25
    )

    return {
        "request_count": request_count,
        "total_likes": total_likes,
        "total_replies": total_replies,
        "demand_score": round(
            demand_score,
            2,
        ),
    }