from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    topics: set[str]
    
class CreatePost(PostBase):
    published: bool = False
    topics: set[str] | None = None

class GetPost(PostBase):
    id: int
    createdAt: datetime
    
    model_config = {
        'from_attributes': True
    }

class UpdatePost(PostBase):
    topics: set[str]