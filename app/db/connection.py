from sqlalchemy import create_engine
from typing import Annotated
from sqlmodel import SQLModel, Session
from fastapi import Depends
from app.models.posts import Post
from app.models.users import User

POSTGRESQL_CONNECTION_STRING="postgresql://postgres:root@localhost/api_learning"

engine = create_engine(POSTGRESQL_CONNECTION_STRING, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("successfully connected to db")
    
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]