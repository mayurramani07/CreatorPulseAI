import numpy as np

from app.models.comment import Comment
from app.services.embedding_service import generate_embeddings


REQUEST_PROTOTYPES = [
    "Please make a video about this topic",
    "Please make a full course about this topic",
    "Can you make a tutorial about this topic?",
    "Can you teach this topic?",
    "Please create a video explaining this topic",
    "I want a video about this topic",
    "Please cover this topic in a future video",
    "Can you make a complete playlist about this topic?",
    "Please make a detailed video on this topic",
]


NON_REQUEST_PROTOTYPES = [
    "This video is amazing",
    "Great video, thank you",
    "I really enjoyed this video",
    "This tutorial helped me a lot",
    "You are an amazing teacher",
    "This was very useful",
    "I love your teaching style",
    "Amazing lecture",
]


def calculate_similarity(
    reference_embedding,
    comment_embedding,
) -> float:
    """
    Calculate cosine similarity between two normalized embeddings.
    """

    return float(
        np.dot(
            reference_embedding,
            comment_embedding,
        )
    )


def detect_content_requests(
    comments: list[Comment],
    candidate_limit: int = 50,
) -> list[dict]:
    """
    Build a high-recall candidate pool for content requests.

    Candidate retrieval uses multiple signals:

    1. Semantic similarity
    2. Comment engagement
    3. Comment recency

    The goal at this stage is recall rather than
    final classification.

    Final topic demand will be calculated later.
    """

    if not comments:
        return []

    comment_texts = [
        comment.text
        for comment in comments
    ]

    all_texts = (
        REQUEST_PROTOTYPES
        + NON_REQUEST_PROTOTYPES
        + comment_texts
    )

    embeddings = generate_embeddings(all_texts)

    request_count = len(REQUEST_PROTOTYPES)
    non_request_count = len(NON_REQUEST_PROTOTYPES)

    request_embeddings = embeddings[
        :request_count
    ]

    non_request_embeddings = embeddings[
        request_count:
        request_count + non_request_count
    ]

    comment_embeddings = embeddings[
        request_count + non_request_count:
    ]

    scored_comments = []

    for comment, comment_embedding in zip(
        comments,
        comment_embeddings,
    ):

        request_similarities = [
            calculate_similarity(
                prototype_embedding,
                comment_embedding,
            )
            for prototype_embedding in request_embeddings
        ]

        non_request_similarities = [
            calculate_similarity(
                prototype_embedding,
                comment_embedding,
            )
            for prototype_embedding in non_request_embeddings
        ]

        request_score = max(request_similarities)
        non_request_score = max(non_request_similarities)

        semantic_score = (
            request_score - non_request_score
        )

        scored_comments.append(
            {
                "comment_id": comment.comment_id,
                "video_id": comment.video_id,
                "text": comment.text,
                "like_count": comment.like_count,
                "reply_count": comment.reply_count,
                "published_at": comment.published_at,
                "request_score": round(
                    request_score,
                    4,
                ),
                "non_request_score": round(
                    non_request_score,
                    4,
                ),
                "semantic_score": round(
                    semantic_score,
                    4,
                ),
            }
        )

    # ---------------------------------------------------------
    # 1. Semantic candidates
    # ---------------------------------------------------------

    semantic_candidates = sorted(
        scored_comments,
        key=lambda item: item["semantic_score"],
        reverse=True,
    )[:candidate_limit]

    # ---------------------------------------------------------
    # 2. Engagement candidates
    # ---------------------------------------------------------

    engagement_candidates = sorted(
        scored_comments,
        key=lambda item: (
            item["like_count"],
            item["reply_count"],
        ),
        reverse=True,
    )[:candidate_limit]

    # ---------------------------------------------------------
    # 3. Recent candidates
    # ---------------------------------------------------------

    recent_candidates = sorted(
        scored_comments,
        key=lambda item: item["published_at"],
        reverse=True,
    )[:candidate_limit]

    # ---------------------------------------------------------
    # Merge candidates
    # ---------------------------------------------------------

    candidates = {}

    for candidate in (
        semantic_candidates
        + engagement_candidates
        + recent_candidates
    ):
        candidates[candidate["comment_id"]] = candidate

    # ---------------------------------------------------------
    # Final ordering
    # ---------------------------------------------------------

    results = sorted(
        candidates.values(),
        key=lambda item: (
            item["semantic_score"],
            item["like_count"],
            item["reply_count"],
        ),
        reverse=True,
    )

    return results