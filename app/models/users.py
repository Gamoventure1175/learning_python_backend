from datetime import datetime
from typing import List, TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.posts import Post


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str
    createdAt: datetime = Field(default_factory=datetime.now)
    posts: List["Post"] = Relationship(back_populates="owner")
    phone_number: str | None = Field(
        min_length=10, max_length=15, regex=r"^\+?[1-9]\d{9, 14$", default=None
    )
