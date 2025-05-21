from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import select
from app.config import settings

from app.db.connection import SessionDep
from app.models.users import User
from app.validation.tokens import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

jwt_secret = settings.secret_key
algorithm = settings.algorithm


def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expires_minutes)
    to_encode.update({"exp": exp})

    encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=algorithm)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[algorithm])
        user_id: int = payload.get("user_id")

        if not user_id:
            raise credentials_exception

        token_data = TokenData(id=user_id)
        return token_data
    except jwt.PyJWTError:
        raise credentials_exception


def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception=credentials_exception)

    user = session.exec(select(User).where(User.id == token_data.id)).first()

    return user
