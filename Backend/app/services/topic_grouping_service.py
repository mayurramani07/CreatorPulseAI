import numpy as np
from app.services.embedding_service import generate_embeddings

def cosine_similarity(
    embedding_a,
    embedding_b,
) -> float:
    """
    Calculate cosine similarity between two embeddings.
    """

    return float(
        np.dot(
            embedding_a,
            embedding_b,
        )
    )


def group_similar_comments(
    comments: list[dict],
    similarity_threshold: float = 0.65,
) -> list[list[dict]]:
    """
    Group semantically similar comments into topic groups.

    Comments with sufficiently similar embeddings
    are placed in the same group.
    """

    if not comments:
        return []

    texts = [
        comment["text"]
        for comment in comments
    ]

    embeddings = generate_embeddings(texts)

    groups = []

    for comment, embedding in zip(
        comments,
        embeddings,
    ):

        added_to_group = False

        for group in groups:
            group_embedding = group["embedding"]
            similarity = cosine_similarity(
                embedding,
                group_embedding,
            )
            if similarity >= similarity_threshold:
                group["comments"].append(comment)
                group["embedding"] = np.mean(
                    [
                        group["embedding"],
                        embedding,
                    ],
                    axis=0,
                )
                added_to_group = True
                break

        if not added_to_group:
            groups.append(
                {
                    "embedding": embedding,
                    "comments": [comment],
                }
            )

    return [
        group["comments"]
        for group in groups
    ]