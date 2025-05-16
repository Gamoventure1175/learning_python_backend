from fastapi import FastAPI, status, Body, HTTPException
from typing import Annotated, List
from contextlib import asynccontextmanager
from pydantic import EmailStr
from sqlmodel import select
from app.models.users import User
from app.utility.password import hash_password
from app.validation.post import CreatePost, GetPost, UpdatePost
from app.db.connection import SessionDep, create_db_and_tables
from app.models.posts import Post
from app.validation.users import CreateUser, UserResponse
from app.routers import post, user, authentication

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)