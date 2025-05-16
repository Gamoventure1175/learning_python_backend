from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import select
from fastapi.security import OAuth2PasswordRequestForm
from app.db.connection import SessionDep
from app.models.users import User
from app.utility.oauth2 import create_access_token
from app.utility.password import verify_password
from app.validation.tokens import Token

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def user_login(
    session: SessionDep, credentials: OAuth2PasswordRequestForm = Depends()
):
    user = session.exec(select(User).where(User.email == credentials.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    encoded_token = create_access_token(data={"user_id": user.id})

    return {"access_token": encoded_token, "token_type": "JWT"}
