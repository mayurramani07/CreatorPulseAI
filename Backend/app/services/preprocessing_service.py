import re

from app.models.comment import Comment


def normalize_text(text: str) -> str:
    """
    Normalize comment text for further analysis.

    This function:
    - converts text to lowercase
    - removes URLs
    - removes excessive whitespace
    """

    text = text.lower()

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def is_low_value_comment(text: str) -> bool:
    """
    Detect obvious low-value comments that are unlikely
    to contain meaningful content demand.
    """

    if not text:
        return True

    # Very short comments
    if len(text) < 4:
        return True

    # Common engagement/noise comments
    noise_patterns = [
        r"^first$",
        r"^second$",
        r"^early$",
        r"^lol+$",
        r"^lmao+$",
        r"^nice$",
        r"^great$",
        r"^cool$",
        r"^wow+$",
        r"^🔥+$",
        r"^😂+$",
        r"^👍+$",
    ]

    for pattern in noise_patterns:
        if re.fullmatch(pattern, text):
            return True

    return False


def preprocess_comments(
    comments: list[Comment],
) -> list[Comment]:
    """
    Clean comments and remove obvious low-value comments.

    The original Comment objects are preserved.
    """

    processed_comments: list[Comment] = []

    for comment in comments:

        normalized_text = normalize_text(comment.text)

        if is_low_value_comment(normalized_text):
            continue

        comment.text = normalized_text

        processed_comments.append(comment)

    return processed_comments