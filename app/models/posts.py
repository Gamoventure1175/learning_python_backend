from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, Relationship, SQLModel

from app.models.users import User


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(default=False)
    topics: List[str] | None = Field(default=None, sa_column=Column(ARRAY(String)))
    createdAt: datetime = Field(default_factory=datetime.now)
    owner_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
        )
    )
    owner: Optional[User] = Relationship(back_populates="posts")
