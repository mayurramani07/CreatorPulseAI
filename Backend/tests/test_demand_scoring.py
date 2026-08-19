from app.services.demand_scoring_service import (
    calculate_topic_demand,
)


aws_comments = [
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
]


cicd_comments = [
    {
        "text": "Please make a complete CI CD tutorial",
        "like_count": 4,
        "reply_count": 0,
    },
    {
        "text": "Can you explain CI CD pipeline?",
        "like_count": 2,
        "reply_count": 0,
    },
]


max_request_count = 3
max_likes = 34
max_replies = 3


aws_score = calculate_topic_demand(
    aws_comments,
    max_request_count,
    max_likes,
    max_replies,
)


cicd_score = calculate_topic_demand(
    cicd_comments,
    max_request_count,
    max_likes,
    max_replies,
)


print("\nAWS")
print(aws_score)


print("\nCI/CD")
print(cicd_score)