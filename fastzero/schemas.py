from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr

from fastzero.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserDB(UserPublic): ...


class UserList(BaseModel):
    users: List[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class FilterTodo(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
