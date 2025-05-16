from datetime import datetime
from typing import List
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, SQLModel

class Post(SQLModel, table=True):    
    id: int | None = Field(default=None, primary_key= True) 
    title: str
    content: str
    published: bool = Field(default=False)
    topics: List[str] | None = Field(default=None, sa_column=Column(ARRAY(String)))
    createdAt: datetime = Field(default_factory=datetime.now)