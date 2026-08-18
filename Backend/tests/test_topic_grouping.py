from app.services.topic_grouping_service import group_similar_comments


comments = [
    {
        "comment_id": "1",
        "text": "Vote for AWS full course",
        "like_count": 26,
        "reply_count": 2,
    },
    {
        "comment_id": "2",
        "text": "Please make a complete AWS course",
        "like_count": 5,
        "reply_count": 0,
    },
    {
        "comment_id": "3",
        "text": "Can you teach AWS from beginner to advanced?",
        "like_count": 3,
        "reply_count": 1,
    },
    {
        "comment_id": "4",
        "text": "Please make a complete CI CD tutorial",
        "like_count": 4,
        "reply_count": 0,
    },
    {
        "comment_id": "5",
        "text": "Can you explain CI CD pipeline?",
        "like_count": 2,
        "reply_count": 0,
    },
    {
        "comment_id": "6",
        "text": "Please make a Kubernetes tutorial",
        "like_count": 1,
        "reply_count": 0,
    },
    {
        "comment_id": "7",
        "text": "Can you teach Kubernetes?",
        "like_count": 1,
        "reply_count": 0,
    },
    {
        "comment_id": "8",
        "text": "Amazing video, thank you!",
        "like_count": 10,
        "reply_count": 1,
    },
]


groups = group_similar_comments(
    comments,
    similarity_threshold=0.65,
)


print("\nNumber of groups:", len(groups))

for index, group in enumerate(groups, start=1):

    print(f"\n--- Group {index} ---")

    for comment in group:
        print(
            f"- {comment['text']}"
            f" | likes={comment['like_count']}"
        )