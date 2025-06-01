from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlmodel import Field, SQLModel


class Vote(SQLModel, table=True):
    post_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("post.id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        ),
    )
    user_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True,
        )
    )
    
    #that user voted for this post post_id <> user_id