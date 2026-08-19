import numpy as np

from app.models.comment import Comment
from app.services.embedding_service import generate_embeddings


REQUEST_PROTOTYPES = [
    "Please make a video about this",
    "Please make a full course about this",
    "Can you make a tutorial about this",
    "Can you teach this topic",
    "Please create a video explaining this",
    "I want a video about this",
    "Please cover this in a future video",
    "Please make a complete playlist about this",
    "Please make more videos about this",
    "Please continue this series",
    "Please extend this playlist",
    "We want to learn this topic",
    "We need a tutorial about this",
    "Please bring a video about this",
    "Can you create content about this",
    "Can you make a detailed video about this",
    "Please create a course about this",
    "Please make content on this topic",
    "I would like a video about this",
    "I would like to learn more about this",
]


NON_REQUEST_PROTOTYPES = [
    # ---------------------------------------------------------
    # Praise / appreciation
    # ---------------------------------------------------------

    "This video is amazing",
    "Great video",
    "Amazing explanation",
    "Very good explanation",
    "This was very useful",
    "This was informative",
    "I really enjoyed this video",
    "You are an amazing teacher",
    "I love your teaching style",
    "Thanks for the explanation",
    "Thank you for this video",
    "Nicely explained",
    "Very helpful video",
    "Great work",
    "Excellent presentation",

    # ---------------------------------------------------------
    # Personal statements / stories
    # ---------------------------------------------------------

    "I learned a lot from this",
    "I watched this video",
    "I have been learning this",
    "This helped me understand the topic",
    "I always watch your videos",
    "I really like your content",
    "This is exactly what I needed",
    "Your explanation helped me",
    "I am learning from your videos",
    "This topic is interesting",

    # ---------------------------------------------------------
    # Questions
    # ---------------------------------------------------------

    "What is this",
    "What does this mean",
    "How does this work",
    "Why does this happen",
    "Can you explain this",
    "What is the difference",
    "Where can I learn this",
    "What are the prerequisites",
    "Is this free",
    "Which tool are you using",
    "Which software are you using",
    "What is the name of this",
    "How can I do this",
]


def cosine_similarity(
    embedding_a,
    embedding_b,
) -> float:
    """
    Calculate cosine similarity between two embeddings.

    generate_embeddings() returns normalized embeddings,
    therefore dot product is sufficient.
    """

    norm_a = np.linalg.norm(
        embedding_a
    )

    norm_b = np.linalg.norm(
        embedding_b
    )

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(
        np.dot(
            embedding_a,
            embedding_b,
        )
        / (norm_a * norm_b)
    )


def detect_content_requests(
    comments: list[Comment],
    candidate_limit: int = 50,
    semantic_threshold: float = 0.12,
    margin_threshold: float = 0.03,
) -> list[dict]:
    """
    Retrieve comments that semantically resemble
    content-request intent.

    The detector does NOT use topic-specific rules.

    It compares every comment against two semantic
    intent spaces:

        REQUEST
        NON_REQUEST

    A comment becomes a candidate only when:

        1. Request similarity is sufficiently strong.
        2. Request similarity is stronger than
           non-request similarity.
        3. The semantic margin is sufficiently large.

    Engagement is used only for ranking candidates.
    """

    if not comments:
        return []

    # ---------------------------------------------------------
    # 1. Prepare texts
    # ---------------------------------------------------------

    comment_texts = [
        comment.text.strip()
        for comment in comments
        if comment.text
        and comment.text.strip()
    ]

    if not comment_texts:
        return []

    # ---------------------------------------------------------
    # 2. Create one embedding batch
    # ---------------------------------------------------------

    all_texts = (
        REQUEST_PROTOTYPES
        + NON_REQUEST_PROTOTYPES
        + comment_texts
    )

    embeddings = generate_embeddings(
        all_texts
    )

    request_count = len(
        REQUEST_PROTOTYPES
    )

    non_request_count = len(
        NON_REQUEST_PROTOTYPES
    )

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

    # ---------------------------------------------------------
    # 3. Score every comment
    # ---------------------------------------------------------

    scored_comments = []

    valid_comments = [
        comment
        for comment in comments
        if comment.text
        and comment.text.strip()
    ]

    for comment, comment_embedding in zip(
        valid_comments,
        comment_embeddings,
    ):

        # -----------------------------------------------------
        # Request semantic similarity
        # -----------------------------------------------------

        request_similarities = [
            cosine_similarity(
                prototype_embedding,
                comment_embedding,
            )
            for prototype_embedding
            in request_embeddings
        ]

        # -----------------------------------------------------
        # Non-request semantic similarity
        # -----------------------------------------------------

        non_request_similarities = [
            cosine_similarity(
                prototype_embedding,
                comment_embedding,
            )
            for prototype_embedding
            in non_request_embeddings
        ]

        request_score = max(
            request_similarities
        )

        non_request_score = max(
            non_request_similarities
        )

        semantic_margin = (
            request_score
            - non_request_score
        )

        # -----------------------------------------------------
        # Candidate decision
        # -----------------------------------------------------

        is_request = (
            request_score
            >= semantic_threshold
            and semantic_margin
            >= margin_threshold
        )

        if not is_request:
            continue

        scored_comments.append(
            {
                "comment_id": (
                    comment.comment_id
                ),
                "video_id": (
                    comment.video_id
                ),
                "text": comment.text,
                "like_count": (
                    comment.like_count
                ),
                "reply_count": (
                    comment.reply_count
                ),
                "published_at": (
                    comment.published_at
                ),
                "request_score": round(
                    request_score,
                    4,
                ),
                "non_request_score": round(
                    non_request_score,
                    4,
                ),
                "semantic_score": round(
                    semantic_margin,
                    4,
                ),
            }
        )

    if not scored_comments:
        return []

    # ---------------------------------------------------------
    # 4. Keep strongest semantic candidates
    # ---------------------------------------------------------

    semantic_candidates = sorted(
        scored_comments,
        key=lambda item: (
            item["semantic_score"],
            item["request_score"],
        ),
        reverse=True,
    )[:candidate_limit]

    if not semantic_candidates:
        return []

    # ---------------------------------------------------------
    # 5. Normalize engagement
    # ---------------------------------------------------------

    max_likes = max(
        item["like_count"]
        for item in semantic_candidates
    )

    max_replies = max(
        item["reply_count"]
        for item in semantic_candidates
    )

    # ---------------------------------------------------------
    # 6. Re-rank using engagement
    # ---------------------------------------------------------

    results = []

    for item in semantic_candidates:

        like_score = (
            item["like_count"]
            / max_likes
            if max_likes > 0
            else 0.0
        )

        reply_score = (
            item["reply_count"]
            / max_replies
            if max_replies > 0
            else 0.0
        )

        # Semantic intent remains dominant.
        candidate_score = (
            item["semantic_score"] * 0.75
            + like_score * 0.15
            + reply_score * 0.10
        )

        item["like_score"] = round(
            like_score,
            4,
        )

        item["reply_score"] = round(
            reply_score,
            4,
        )

        item["candidate_score"] = round(
            candidate_score,
            4,
        )

        results.append(item)

    # ---------------------------------------------------------
    # 7. Final ranking
    # ---------------------------------------------------------

    return sorted(
        results,
        key=lambda item: (
            item["candidate_score"],
            item["semantic_score"],
        ),
        reverse=True,
    )