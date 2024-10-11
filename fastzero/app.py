from http import HTTPStatus
from typing import List

from fastapi import FastAPI, HTTPException

from fastzero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title="FastFromZero")

fakedb_list: List[UserPublic] = list[UserPublic]()


@app.post("/users/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema) -> UserPublic:
    newUser = UserDB(id=len(fakedb_list) + 1, **user.model_dump())
    fakedb_list.append(newUser)
    return newUser


@app.get("/users/", response_model=UserList, status_code=HTTPStatus.OK)
def get_users() -> UserList:
    return UserList(users=fakedb_list)


@app.get(
    "/users/{user_id}", response_model=UserPublic, status_code=HTTPStatus.OK
)
def get_user_by_id(user_id: int) -> UserPublic:
    if user_id < 1 or user_id > len(fakedb_list):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    return fakedb_list[user_id - 1]


@app.put(
    "/users/{user_id}", response_model=UserPublic, status_code=HTTPStatus.OK
)
def update_user(user_id: int, user: UserSchema) -> UserPublic:
    if user_id < 1 or user_id > len(fakedb_list):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    oldUser = UserDB(id=user_id, **user.model_dump())
    fakedb_list[user_id - 1] = oldUser
    return oldUser


@app.delete(
    "/users/{user_id}", response_model=Message, status_code=HTTPStatus.OK
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(fakedb_list):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    fakedb_list.pop(user_id - 1)
    return Message(message="User deleted!")
