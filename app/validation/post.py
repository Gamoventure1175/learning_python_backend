from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

from app.validation.users import UserResponse


class PostBase(BaseModel):
    title: str
    content: str
    published: bool
    topics: set[str]


class GetPost(PostBase):
    id: int
    createdAt: datetime
    owner_id: int
    owner: UserResponse
    model_config = {"from_attributes": True}


class PostWithVotes(BaseModel):
    post: GetPost
    votes: int


class CreatePost(PostBase):
    published: bool = False
    topics: set[str] | None = None


class UpdatePost(PostBase):
    topics: set[str]
