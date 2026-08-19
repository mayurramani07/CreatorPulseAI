def calculate_topic_signals(
    topic_comments: list[dict],
) -> dict:
    """
    Calculate raw demand signals for one topic.
    """

    request_count = len(topic_comments)

    total_likes = sum(
        comment.get("like_count", 0)
        for comment in topic_comments
    )

    total_replies = sum(
        comment.get("reply_count", 0)
        for comment in topic_comments
    )

    return {
        "request_count": request_count,
        "total_likes": total_likes,
        "total_replies": total_replies,
    }


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


def calculate_demand_scores(
    topic_groups: dict[str, list[dict]],
) -> list[dict]:
    """
    Calculate demand scores for all topic groups.

    Weighting:
    - 50% request frequency
    - 35% likes
    - 15% replies
    """

    if not topic_groups:
        return []

    topic_signals = {}

    for topic, comments in topic_groups.items():

        topic_signals[topic] = calculate_topic_signals(
            comments
        )


    max_request_count = max(
        signals["request_count"]
        for signals in topic_signals.values()
    )

    max_likes = max(
        signals["total_likes"]
        for signals in topic_signals.values()
    )

    max_replies = max(
        signals["total_replies"]
        for signals in topic_signals.values()
    )

    results = []

    for topic, signals in topic_signals.items():

        request_score = normalize(
            signals["request_count"],
            max_request_count,
        )

        like_score = normalize(
            signals["total_likes"],
            max_likes,
        )

        reply_score = normalize(
            signals["total_replies"],
            max_replies,
        )

        demand_score = (
            request_score * 0.50
            + like_score * 0.35
            + reply_score * 0.15
        )

        results.append(
            {
                "topic": topic,
                "request_count": signals["request_count"],
                "total_likes": signals["total_likes"],
                "total_replies": signals["total_replies"],
                "request_score": round(
                    request_score,
                    4,
                ),
                "like_score": round(
                    like_score,
                    4,
                ),
                "reply_score": round(
                    reply_score,
                    4,
                ),
                "demand_score": round(
                    demand_score,
                    4,
                ),
            }
        )
    results.sort(
        key=lambda item: item["demand_score"],
        reverse=True,
    )
    return results