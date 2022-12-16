from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    email: str

    class Config:
        orm_mode = True
        fields = {'password': {'exclude': True}}


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class Post(PostBase):
    created_at: datetime
    author: User

    class Config:
        orm_mode = True
        fields = {'rating': {'exclude': True}}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class UserPosts(UserBase):
    email: str
    posts: list[Post] = []

    class Config:
        orm_mode = True
        fields = {'password': {'exclude': True}}


class VoteBase(BaseModel):
    post_id: int
    post_dir: bool  # 0 decrease post likes, 1 increase post likes
