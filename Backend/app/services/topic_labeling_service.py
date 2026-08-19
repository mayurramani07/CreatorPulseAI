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


def get_representative_comment(
    comments: list[dict],
) -> dict | None:
    """
    Find the comment that is most representative
    of the entire topic group.

    The representative comment is the comment whose
    embedding is most similar to the average embedding
    of the group.
    """

    if not comments:
        return None

    texts = [
        comment.get("text", "")
        for comment in comments
    ]

    embeddings = generate_embeddings(texts)

    # Calculate the center of the topic group.
    group_embedding = np.mean(
        embeddings,
        axis=0,
    )

    best_index = 0
    best_similarity = -1.0

    for index, embedding in enumerate(embeddings):

        similarity = cosine_similarity(
            embedding,
            group_embedding,
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_index = index

    return comments[best_index]


def get_topic_label(
    comments: list[dict],
) -> str:
    """
    Generate a topic label using the most
    representative comment.
    """

    representative_comment = (
        get_representative_comment(comments)
    )

    if not representative_comment:
        return "Unknown"

    return representative_comment.get(
        "text",
        "Unknown",
    )