from typing import Annotated
from fastapi import APIRouter, Depends,status, HTTPException
from sqlmodel import select
from fastapi.security import OAuth2PasswordRequestForm
from app.db.connection import SessionDep
from app.models.users import User
from app.utility.oauth import create_access_token
from app.utility.password import verify_password
from app.validation.users import UserLogin

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(session: SessionDep, credentials: OAuth2PasswordRequestForm = Depends()):
    user = session.exec(select(User).where(User.email == credentials.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    encoded_token = create_access_token(data={"userId": user.id})
    
    return {"accessToken": encoded_token, "token_type": "JWT"}