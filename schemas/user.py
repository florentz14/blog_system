from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from .profile import ProfileCreate, ProfileRead


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    profile: Optional[ProfileCreate] = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserReadWithProfile(UserRead):
    profile: ProfileRead
