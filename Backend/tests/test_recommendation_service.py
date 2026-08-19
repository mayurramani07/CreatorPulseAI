from app.services.recommendation_service import (
    build_topic_recommendations,
)


topic_groups = {

    "aws_group": [
        {
            "text": "Vote for AWS full course",
            "like_count": 26,
            "reply_count": 2,
        },
        {
            "text": "Please make a complete AWS course",
            "like_count": 5,
            "reply_count": 0,
        },
        {
            "text": "Can you teach AWS from beginner to advanced?",
            "like_count": 3,
            "reply_count": 1,
        },
    ],

    "cicd_group": [
        {
            "text": "Please make a complete CI/CD tutorial",
            "like_count": 4,
            "reply_count": 0,
        },
        {
            "text": "Can you explain CI/CD pipeline?",
            "like_count": 2,
            "reply_count": 0,
        },
    ],

    "kubernetes_group": [
        {
            "text": "Please make a Kubernetes tutorial",
            "like_count": 1,
            "reply_count": 0,
        },
        {
            "text": "Can you teach Kubernetes?",
            "like_count": 1,
            "reply_count": 0,
        },
    ],
}


recommendations = build_topic_recommendations(
    topic_groups
)


print("\nFinal Topic Recommendations")
print("===========================")


for index, recommendation in enumerate(
    recommendations,
    start=1,
):

    print(
        f"\n{index}. "
        f"{recommendation['topic']}"
    )

    print(
        "   Representative:",
        recommendation[
            "representative_comment"
        ],
    )

    print(
        "   Requests:",
        recommendation["request_count"],
    )

    print(
        "   Likes:",
        recommendation["total_likes"],
    )

    print(
        "   Replies:",
        recommendation["total_replies"],
    )

    print(
        "   Demand Score:",
        recommendation["demand_score"],
    )