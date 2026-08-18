from googleapiclient.discovery import build

from app.config import YOUTUBE_API_KEY
from app.models.comment import Comment


youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY,
)


def get_video(video_id: str):
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id,
    ).execute()

    return response


def get_comments(
    video_id: str,
    max_comments: int = 500,
) -> list[Comment]:
    """
    Collect top-level YouTube comments using pagination.

    YouTube returns a maximum of 100 comment threads per API request.
    This function keeps requesting pages until:

    1. max_comments is reached, or
    2. YouTube has no more pages.
    """

    comments: list[Comment] = []
    next_page_token = None

    while len(comments) < max_comments:

        remaining = max_comments - len(comments)
        page_size = min(100, remaining)

        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=page_size,
            textFormat="plainText",
            pageToken=next_page_token,
        ).execute()

        items = response.get("items", [])

        if not items:
            break

        for item in items:
            comment = parse_comment(item)

            comments.append(comment)

            if len(comments) >= max_comments:
                break

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return comments


def parse_comment(item: dict) -> Comment:
    """
    Convert a YouTube comment thread into our Comment model.
    """

    thread_snippet = item["snippet"]
    comment_snippet = thread_snippet["topLevelComment"]["snippet"]

    return Comment(
        comment_id=item["id"],
        video_id=comment_snippet["videoId"],
        text=comment_snippet["textOriginal"],
        like_count=comment_snippet["likeCount"],
        published_at=comment_snippet["publishedAt"],
        updated_at=comment_snippet["updatedAt"],
        reply_count=thread_snippet["totalReplyCount"],
    )