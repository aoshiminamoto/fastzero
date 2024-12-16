from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import Todo, User
from fastzero.schemas import (
    FilterTodo,
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fastzero.security import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

TFilters = Annotated[FilterTodo, Query()]
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=TodoPublic, status_code=HTTPStatus.CREATED)
def create_todo(
    todo: TodoSchema,
    session: T_Session,
    user: T_CurrentUser,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get("/", response_model=TodoList)
def list_todos(
    user: T_CurrentUser,
    session: T_Session,
    filters: TFilters,
):
    query = select(Todo).where(Todo.user_id == user.id)

    if filters.title:
        query = query.filter(Todo.title.contains(filters.title))

    if filters.description:
        query = query.filter(Todo.description.contains(filters.description))

    if filters.state:
        query = query.filter(Todo.state == filters.state)

    todos = session.scalars(
        query.offset(filters.offset).limit(filters.limit)
    ).all()

    return {"todos": todos}


@router.get("/{todo_id}", response_model=TodoPublic, status_code=HTTPStatus.OK)
def get_todo_by_id(
    todo_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
) -> TodoPublic:
    db_todo = session.scalar(select(Todo).where(Todo.id == todo_id))

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Todo not found"
        )

    return db_todo


@router.delete("/{todo_id}", response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: T_CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Task not found."
        )

    session.delete(todo)
    session.commit()

    return {"message": "Task has been deleted successfully."}


@router.patch("/{todo_id}", response_model=TodoPublic)
def patch_todo(
    todo_id: int,
    todo: TodoUpdate,
    session: T_Session,
    user: T_CurrentUser,
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Task not found."
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
