from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    description: str
    id: Optional[int]

class UserResponseSchema(BaseModel):

    id: int
    image_url: str
    description: str
    creation_date: datetime

    class Config:
        from_attributes = True