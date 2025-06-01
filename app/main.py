from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.connection import SessionDep, create_db_and_tables
from app.routers import post, user, authentication, vote
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return "Hello World"


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)

# issi file
