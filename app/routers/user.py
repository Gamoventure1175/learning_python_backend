from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import EmailStr
from app.utility.oauth2 import get_current_user
from app.utility.password import hash_password
from app.db.connection import SessionDep
from app.models.users import User
from app.validation.users import CreateUser, UserResponse
from sqlmodel import select

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(session: SessionDep, user: CreateUser):
    userModel = user.model_dump()
    hashedPassword = hash_password(userModel["password"])
    userModel["password"] = hashedPassword
    userData = User(**userModel)
    session.add(userData)
    session.commit()
    session.refresh(userData)
    return userData


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_current_user_information(session: SessionDep, current_user: UserResponse = Depends(get_current_user)):
    user = session.exec(select(User).where(User.id == current_user.id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find user with the given email",
        )
    return user
