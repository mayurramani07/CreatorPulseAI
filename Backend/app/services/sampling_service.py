from datetime import datetime, timezone

from app.models.comment import Comment


def calculate_engagement_score(comment: Comment) -> float:
    """
    Calculate a simple engagement score for a comment.

    Likes are currently our strongest engagement signal.
    Replies are included as a secondary signal.
    """

    return comment.like_count + (comment.reply_count * 2)


def sort_by_engagement(comments: list[Comment]) -> list[Comment]:
    """
    Sort comments from highest to lowest engagement.
    """

    return sorted(
        comments,
        key=calculate_engagement_score,
        reverse=True,
    )


def sort_by_recency(comments: list[Comment]) -> list[Comment]:
    """
    Sort comments from newest to oldest.
    """

    return sorted(
        comments,
        key=lambda comment: comment.published_at,
        reverse=True,
    )

def build_sample(
    comments: list[Comment],
    sample_size: int = 300,
) -> list[Comment]:

    if len(comments) <= sample_size:
        return comments

    engagement_sorted = sort_by_engagement(comments)
    recent_sorted = sort_by_recency(comments)

    engaged_count = int(sample_size * 0.4)
    recent_count = int(sample_size * 0.3)

    selected = {}

    # 40% highly engaged comments
    for comment in engagement_sorted[:engaged_count]:
        selected[comment.comment_id] = comment

    # 30% recent comments
    for comment in recent_sorted[:recent_count]:
        selected[comment.comment_id] = comment

    # Remaining slots
    for comment in comments:
        if len(selected) >= sample_size:
            break

        selected[comment.comment_id] = comment

    return list(selected.values())

