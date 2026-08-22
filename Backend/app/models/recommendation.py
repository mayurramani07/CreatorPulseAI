from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    analysis_id: Mapped[int] = mapped_column(
        ForeignKey("analyses.id"),
        nullable=False,
        index=True,
    )

    topic: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    demand_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    request_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    total_likes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    total_replies: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    representative_comment: Mapped[str] = mapped_column(
        String(2000),
        nullable=True,
    )

    analysis = relationship(
        "Analysis",
        back_populates="recommendations",
    )