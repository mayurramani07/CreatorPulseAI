import numpy as np

from app.services.embedding_service import generate_embeddings


def cosine_similarity(
    embedding_a,
    embedding_b,
) -> float:
    """
    Calculate cosine similarity between two embeddings.
    """

    norm_a = np.linalg.norm(embedding_a)
    norm_b = np.linalg.norm(embedding_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(
        np.dot(embedding_a, embedding_b)
        / (norm_a * norm_b)
    )


def group_similar_comments(
    comments: list[dict],
    similarity_threshold: float = 0.68,
) -> list[list[dict]]:
    """
    Group semantically similar content-request comments.

    Grouping is based entirely on embeddings.

    No topic-specific rules are used.
    """

    if not comments:
        return []

    texts = [
        comment.get("text", "").strip()
        for comment in comments
    ]

    valid_items = [
        (comment, text)
        for comment, text in zip(
            comments,
            texts,
        )
        if text
    ]

    if not valid_items:
        return []

    valid_comments = [
        item[0]
        for item in valid_items
    ]

    valid_texts = [
        item[1]
        for item in valid_items
    ]

    embeddings = generate_embeddings(
        valid_texts
    )

    groups = []

    for comment, embedding in zip(
        valid_comments,
        embeddings,
    ):

        best_group = None
        best_similarity = -1.0

        for group in groups:

            similarity = cosine_similarity(
                embedding,
                group["embedding"],
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_group = group

        if (
            best_group is not None
            and best_similarity >= similarity_threshold
        ):

            best_group["comments"].append(
                comment
            )

            # Update semantic center.
            best_group["embedding"] = np.mean(
                [
                    best_group["embedding"],
                    embedding,
                ],
                axis=0,
            )

        else:

            groups.append(
                {
                    "embedding": embedding,
                    "comments": [
                        comment
                    ],
                }
            )

    return [
        group["comments"]
        for group in groups
    ]