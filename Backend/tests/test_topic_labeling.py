from app.services.topic_labeling_service import (
    get_topic_label,
)


aws_comments = [
    {
        "text": "Vote for AWS full course",
    },
    {
        "text": "Please make a complete AWS course",
    },
    {
        "text": "Can you teach AWS from beginner to advanced?",
    },
]


cicd_comments = [
    {
        "text": "Please make a complete CI/CD tutorial",
    },
    {
        "text": "Can you explain CI/CD pipeline?",
    },
]


kubernetes_comments = [
    {
        "text": "Please make a Kubernetes tutorial",
    },
    {
        "text": "Can you teach Kubernetes?",
    },
]


print(
    "AWS:",
    get_topic_label(aws_comments),
)

print(
    "CI/CD:",
    get_topic_label(cicd_comments),
)

print(
    "Kubernetes:",
    get_topic_label(kubernetes_comments),
)