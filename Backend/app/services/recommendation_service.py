from app.services.demand_scoring_service import (
    calculate_demand_scores,
)


def build_topic_recommendations(
    topic_groups: dict[str, list[dict]],
) -> list[dict]:
    """
    Build final ranked recommendations from
    LLM-generated semantic topic groups.

    Topic discovery is handled by the LLM.
    Demand scoring is handled by Python.
    """

    if not topic_groups:
        return []

    demand_results = calculate_demand_scores(
        topic_groups
    )

    recommendations = []


    for result in demand_results:

        topic = result["topic"]

        comments = topic_groups.get(
            topic,
            [],
        )

        if not comments:
            continue

        # Choose the highest-engagement comment
        representative_comment = max(
            comments,
            key=lambda comment: (
                comment.get(
                    "like_count",
                    0,
                ),
                comment.get(
                    "reply_count",
                    0,
                ),
            ),
        )

        recommendations.append(
            {
                "topic": topic,

                "representative_comment": (
                    representative_comment.get(
                        "text",
                        "",
                    )
                ),

                "request_count": result[
                    "request_count"
                ],

                "total_likes": result[
                    "total_likes"
                ],

                "total_replies": result[
                    "total_replies"
                ],

                "request_score": result[
                    "request_score"
                ],

                "like_score": result[
                    "like_score"
                ],

                "reply_score": result[
                    "reply_score"
                ],

                "demand_score": result[
                    "demand_score"
                ],
            }
        )

    return recommendations