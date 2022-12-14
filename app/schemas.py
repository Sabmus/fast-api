from pydantic import BaseModel
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

    class Config:
        orm_mode = True
        fields = {'rating': {'exclude': True}}
