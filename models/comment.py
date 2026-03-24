from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .post import Post
    from .user import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_name: Mapped[str] = mapped_column(String(100), nullable=False)
    author_email: Mapped[Optional[str]] = mapped_column(String(100))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comments.id"))
    is_approved: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    post: Mapped["Post"] = relationship(back_populates="comments")
    user: Mapped[Optional["User"]] = relationship(back_populates="comments")
    parent: Mapped[Optional["Comment"]] = relationship(
        remote_side=[id],
        back_populates="replies",
        foreign_keys=[parent_id],
    )
    replies: Mapped[List["Comment"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id}, author='{self.author_name}')>"
