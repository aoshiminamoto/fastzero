from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import Token
from fastzero.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])
T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login(session: T_Session, form_data: T_OAuth2Form) -> Token:
    dbuser = session.scalar(select(User).where((User.username == form_data.username)))

    if not (dbuser and verify_password(form_data.password, dbuser.password)):
        raise HTTPException(
            detail="Incorrect username or password",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    access_token = create_access_token(data={"sub": dbuser.username})
    return Token(access_token=access_token, token_type="Bearer")


@router.post("/token/refresh", response_model=Token, status_code=status.HTTP_200_OK)
def refresh_access_token(user: User = Depends(get_current_user)) -> Token:
    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="Bearer")
