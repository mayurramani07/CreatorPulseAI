from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    video_id: Mapped[int] = mapped_column(
        ForeignKey("videos.id"),
        nullable=False,
        index=True,
    )

    processed_comments: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    content_request_candidates: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    topic_groups: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    video = relationship(
        "Video",
        back_populates="analyses",
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="analysis",
        cascade="all, delete-orphan",
    )