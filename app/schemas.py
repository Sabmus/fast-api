from pydantic import BaseModel, SecretStr, EmailStr
from typing import Optional
from datetime import datetime

# schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default True value
    rating: Optional[int] = None  # optional field


class PostResponse(Post):
    created_at: datetime

    # for converting a sqlalchemy model to pydantinc model (?) (according to yt tuto)
    class Config:
        orm_mode = True
        fields = {'rating': {'exclude': True}}


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserCreate):
    password: SecretStr

    class Config:
        orm_mode = True
