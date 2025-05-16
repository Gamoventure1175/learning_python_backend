from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import select

from app.db.connection import SessionDep
from app.models.users import User
from app.validation.tokens import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

JWT_SECRET = "b9d7d05210faf8094381041e9b8b941212b0dfb6fe8dfa9c2eedb09af39070c2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUETS = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUETS)
    to_encode.update({"exp": exp})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
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
