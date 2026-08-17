from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    comment_id: str
    video_id: str
    text: str
    like_count: int
    published_at: datetime
    updated_at: datetime
    reply_count: int