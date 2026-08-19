from app.services.demand_scoring_service import (
    calculate_demand_scores,
)

from app.services.topic_labeling_service import (
    get_topic_label,
    get_representative_comment,
)


def build_topic_recommendations(
    topic_groups: dict[str, list[dict]],
) -> list[dict]:
    """
    Build final ranked topic recommendations.
    """

    if not topic_groups:
        return []

    demand_results = calculate_demand_scores(
        topic_groups
    )

    recommendations = []

    for result in demand_results:

        topic_key = result["topic"]

        comments = topic_groups[
            topic_key
        ]

        # Use the MiniLM-selected representative comment.
        representative_comment = (
            get_representative_comment(comments)
        )

        topic_label = get_topic_label(
            comments
        )

        recommendations.append(
            {
                "topic": topic_label,
                "representative_comment": (
                    representative_comment.get(
                        "text",
                        "",
                    )
                    if representative_comment
                    else ""
                ),
                "request_count": (
                    result["request_count"]
                ),
                "total_likes": (
                    result["total_likes"]
                ),
                "total_replies": (
                    result["total_replies"]
                ),
                "request_score": (
                    result["request_score"]
                ),
                "like_score": (
                    result["like_score"]
                ),
                "reply_score": (
                    result["reply_score"]
                ),
                "demand_score": (
                    result["demand_score"]
                ),
            }
        )

    return recommendations