from app.services.demand_scoring_service import (
    calculate_demand_scores,
)

from app.services.topic_labeling_service import (
    get_representative_comment,
    get_topic_label,
)


def build_topic_recommendations(
    topic_groups,
) -> list[dict]:
    """
    Build ranked topic recommendations.

    Supports both:

    1. Existing topic grouping output:
       [
           [comment, comment],
           [comment, comment],
       ]

    2. Dictionary-based test input:
       {
           "aws_group": [comment, comment],
           "cicd_group": [comment, comment],
       }
    """

    if not topic_groups:
        return []

    # ---------------------------------------------------------
    # Normalize input into:
    #
    # {
    #     "group_1": [...],
    #     "group_2": [...],
    # }
    # ---------------------------------------------------------

    if isinstance(topic_groups, list):

        grouped_comments = {
            f"group_{index + 1}": comments
            for index, comments in enumerate(
                topic_groups
            )
            if comments
        }

    elif isinstance(topic_groups, dict):

        grouped_comments = {
            topic: comments
            for topic, comments in topic_groups.items()
            if comments
        }

    else:
        raise TypeError(
            "topic_groups must be a list or dictionary"
        )

    if not grouped_comments:
        return []

    # ---------------------------------------------------------
    # Calculate demand scores
    # ---------------------------------------------------------

    demand_results = calculate_demand_scores(
        grouped_comments
    )

    recommendations = []

    # ---------------------------------------------------------
    # Build final recommendation objects
    # ---------------------------------------------------------

    for result in demand_results:

        group_key = result["topic"]

        comments = grouped_comments[
            group_key
        ]

        representative_comment = (
            get_representative_comment(
                comments
            )
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
