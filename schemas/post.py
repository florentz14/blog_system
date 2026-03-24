from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    author_id: int
    category_id: Optional[int] = None
    is_published: bool = False


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    content: str
    summary: Optional[str] = None
    author_id: int
    category_id: Optional[int] = None
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
