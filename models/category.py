from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .post import Post


class Category(Base):
    """Thematic category for posts (flat taxonomy; optional one category per post)."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))

    posts: Mapped[List["Post"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"<Category(name={self.name!r}, slug={self.slug!r})>"
