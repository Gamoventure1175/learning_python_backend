from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.connection import SessionDep, create_db_and_tables
from app.routers import post, user, authentication
from app.config import settings

print(settings.database_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
