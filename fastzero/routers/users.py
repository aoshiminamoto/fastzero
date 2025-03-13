from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as StatusCode
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import Message, UserList, UserPublic, UserSchema
from fastzero.security import (
    get_current_user,
    get_pasword_hash,
)

router = APIRouter(prefix="/users", tags=["users"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=UserPublic, status_code=StatusCode.HTTP_201_CREATED)
def create_user(user: UserSchema, session: T_Session) -> UserPublic:
    dbuser = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if dbuser:
        if dbuser.username == user.username:
            raise HTTPException(
                detail="Username already exists",
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
            )

        if dbuser.email == user.email:
            raise HTTPException(
                detail="Email already exists",
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
            )

    dbuser = User(
        email=user.email,
        username=user.username,
        password=get_pasword_hash(user.password),
    )

    session.add(dbuser)
    session.commit()

    session.refresh(dbuser)
    return dbuser


@router.get("/", response_model=UserList, status_code=StatusCode.HTTP_200_OK)
def get_users(current_user: T_CurrentUser, session: T_Session, limit: int = 20, offset: int = 0) -> UserList:
    user_list = session.scalars(select(User).limit(limit).offset(offset))
    return UserList(users=user_list)


@router.get("/{user_id}", response_model=UserPublic, status_code=StatusCode.HTTP_200_OK)
def get_user_by_id(user_id: int, session: T_Session, current_user: T_CurrentUser) -> UserPublic:
    dbuser = session.scalar(select(User).where(User.id == user_id))

    if not dbuser:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND, detail="User not found")

    return dbuser


@router.put("/{user_id}", response_model=UserPublic, status_code=StatusCode.HTTP_200_OK)
def update_user(user_id: int, user: UserSchema, session: T_Session, current_user: T_CurrentUser) -> UserPublic:
    if current_user.id != user_id:
        raise HTTPException(
            detail="Not enough permissions",
            status_code=StatusCode.HTTP_403_FORBIDDEN,
        )

    current_user.password = get_pasword_hash(current_user.password)
    session.add(current_user)
    session.commit()

    session.refresh(current_user)
    return current_user


@router.delete("/{user_id}", response_model=Message, status_code=StatusCode.HTTP_200_OK)
def delete_user(user_id: int, session: T_Session, current_user: T_CurrentUser) -> Message:
    if current_user.id != user_id:
        raise HTTPException(
            detail="Not enough permissions",
            status_code=StatusCode.HTTP_403_FORBIDDEN,
        )

    session.delete(current_user)
    session.commit()

    return Message(message="User deleted")
