from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    content: str
    author_name: str
    author_email: Optional[str] = None
    post_id: int
    user_id: Optional[int] = None
    parent_id: Optional[int] = None


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    author_name: str
    author_email: Optional[str] = None
    post_id: int
    user_id: Optional[int] = None
    parent_id: Optional[int] = None
    is_approved: str
    created_at: datetime
    updated_at: Optional[datetime] = None
