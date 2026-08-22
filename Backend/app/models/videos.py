from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    youtube_video_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    channel_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    thumbnail_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=True,
    )

    view_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    like_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    comment_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    analyses = relationship(
        "Analysis",
        back_populates="video",
        cascade="all, delete-orphan",
    )