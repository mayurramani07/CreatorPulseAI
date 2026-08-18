from app.models.comment import Comment


def calculate_engagement_score(comment: Comment) -> float:
    """
    Calculate an engagement score for a comment.

    Likes are the strongest engagement signal.
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


def determine_sample_size(total_comments: int) -> int:
    """
    Determine the number of comments that should be analyzed
    based on the total number of available comments.

    Strategy:

    < 1,000 comments
        -> Analyze all available comments

    1,000 - 10,000
        -> Analyze up to 1,000 comments

    10,000 - 100,000
        -> Analyze up to 1,500 comments

    > 100,000
        -> Analyze up to 2,000 comments

    The upper limits prevent the downstream AI pipeline
    from becoming unnecessarily expensive or slow.
    """

    if total_comments <= 0:
        return 0

    if total_comments < 1_000:
        return total_comments

    if total_comments <= 10_000:
        return 1_000

    if total_comments <= 100_000:
        return 1_500

    return 2_000


def build_sample(
    comments: list[Comment],
    sample_size: int | None = None,
) -> list[Comment]:
    """
    Build a representative sample of comments.

    The sample combines:

    - highly engaged comments
    - recent comments
    - additional comments for broader coverage
    """

    if not comments:
        return []

    total_comments = len(comments)

    if sample_size is None:
        sample_size = determine_sample_size(total_comments)

    if total_comments <= sample_size:
        return comments

    engagement_sorted = sort_by_engagement(comments)
    recent_sorted = sort_by_recency(comments)

    engaged_count = int(sample_size * 0.4)
    recent_count = int(sample_size * 0.3)

    selected: dict[str, Comment] = {}

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