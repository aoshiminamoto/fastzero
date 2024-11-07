from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, PyJWTError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import TokenData
from fastzero.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()
oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_pasword_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    exp: datetime = datetime.now(tz=ZoneInfo("UTC"))
    exp += timedelta(minutes=settings.ACCESSTOKENEXPIRE)

    to_encode = data.copy()
    to_encode.update({"exp": exp})
    token = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return token


def get_current_user(
    token: str = Depends(oauth_schema),
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
        detail="Could not validate credentials",
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username: str = payload.get("sub")

        if not username:
            raise credentials_exception

        token_data = TokenData(username=username)

    except ExpiredSignatureError:
        raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.username == token_data.username)
    )

    if not user:
        raise credentials_exception

    return user
