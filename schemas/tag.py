from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
