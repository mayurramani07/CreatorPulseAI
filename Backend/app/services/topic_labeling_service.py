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
    Return the comment closest to the semantic
    center of the topic group.
    """

    if not comments:
        return None

    valid_comments = [
        comment
        for comment in comments
        if comment.get("text", "").strip()
    ]

    if not valid_comments:
        return None

    texts = [
        comment["text"]
        for comment in valid_comments
    ]

    embeddings = generate_embeddings(
        texts
    )

    group_embedding = np.mean(
        embeddings,
        axis=0,
    )

    similarities = [
        cosine_similarity(
            embedding,
            group_embedding,
        )
        for embedding in embeddings
    ]

    best_index = int(
        np.argmax(similarities)
    )

    return valid_comments[
        best_index
    ]


def _generate_phrase_candidates(
    text: str,
) -> list[str]:
    """
    Generate candidate phrases without using
    topic-specific words or stop-word rules.

    The semantic model decides which candidate
    represents the topic.
    """

    words = text.split()

    candidates = []

    # Keep original meaningful phrases.
    for size in (1, 2, 3):

        for index in range(
            len(words) - size + 1
        ):

            phrase = " ".join(
                words[
                    index:index + size
                ]
            ).strip(
                ".,!?;:\"'()[]{}"
            )

            if phrase:
                candidates.append(
                    phrase
                )

    return list(
        dict.fromkeys(
            candidates
        )
    )


def get_topic_label(
    comments: list[dict],
) -> str:
    """
    Generate a semantic topic label.

    No hardcoded topic names.
    No stop-word filtering.
    No AWS/RAG/CI-CD specific rules.
    """

    if not comments:
        return "Unknown"

    valid_comments = [
        comment
        for comment in comments
        if comment.get("text", "").strip()
    ]

    if not valid_comments:
        return "Unknown"

    texts = [
        comment["text"]
        for comment in valid_comments
    ]

    # ---------------------------------------------------------
    # 1. Generate embeddings for complete comments
    # ---------------------------------------------------------

    comment_embeddings = generate_embeddings(
        texts
    )

    group_embedding = np.mean(
        comment_embeddings,
        axis=0,
    )

    # ---------------------------------------------------------
    # 2. Generate candidate phrases
    # ---------------------------------------------------------

    candidates = []

    for text in texts:

        candidates.extend(
            _generate_phrase_candidates(
                text
            )
        )

    candidates = list(
        dict.fromkeys(
            candidates
        )
    )

    if not candidates:
        return "Unknown"

    # ---------------------------------------------------------
    # 3. Embed candidate phrases
    # ---------------------------------------------------------

    candidate_embeddings = (
        generate_embeddings(
            candidates
        )
    )

    # ---------------------------------------------------------
    # 4. Semantic ranking
    # ---------------------------------------------------------

    scored_candidates = []

    for phrase, embedding in zip(
        candidates,
        candidate_embeddings,
    ):

        similarity = cosine_similarity(
            embedding,
            group_embedding,
        )

        scored_candidates.append(
            {
                "phrase": phrase,
                "similarity": similarity,
            }
        )

    scored_candidates.sort(
        key=lambda item: item[
            "similarity"
        ],
        reverse=True,
    )

    # ---------------------------------------------------------
    # 5. Prefer concise semantic concepts
    # ---------------------------------------------------------

    best_phrase = None
    best_score = -1.0

    for item in scored_candidates:

        phrase = item["phrase"]
        similarity = item["similarity"]

        word_count = len(
            phrase.split()
        )

        # Avoid selecting the entire sentence.
        if word_count > 4:
            continue

        # Slight preference for 1-3 word concepts.
        if word_count == 1:
            score = similarity

        elif word_count == 2:
            score = similarity + 0.015

        elif word_count == 3:
            score = similarity + 0.01

        else:
            score = similarity - 0.01

        if score > best_score:

            best_score = score
            best_phrase = phrase

    if not best_phrase:
        best_phrase = scored_candidates[0][
            "phrase"
        ]

    return best_phrase.upper()