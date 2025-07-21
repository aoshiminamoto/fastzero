from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fastzero.app import app
from fastzero.database import get_session
from fastzero.factories import TodoFactory, UserFactory
from fastzero.models import User, table_registry
from fastzero.schemas import TodoPublic
from fastzero.security import get_password_hash


@pytest.fixture
def client(session: Session) -> Generator[TestClient, Any, None]:
    def get_fake_session():
        return session

    app.dependency_overrides[get_session] = get_fake_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, Any, None]:
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine) -> Generator[Session, Any, None]:
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session: Session) -> User:
    pwd = "#1234"

    user_test = User(**{
        "email": "J@test.com",
        "username": "joaozinho",
        "password": get_password_hash(pwd),
    })

    session.add(user_test)

    session.commit()
    session.refresh(user_test)
    user_test.clean_password = pwd  # Monkey Patch

    return user_test


@pytest.fixture
def other_user(session: Session) -> User:
    pwd = "#1234"

    user_test = UserFactory(password=get_password_hash(pwd))
    session.add(user_test)
    session.commit()

    session.refresh(user_test)
    user_test.clean_password = pwd  # Monkey Patch

    return user_test


@pytest.fixture
def fake_todo(user: User) -> TodoPublic:
    todo_test = TodoFactory(user_id=user.id)
    return todo_test


@pytest.fixture
def todo(session: Session, fake_todo: TodoPublic) -> TodoPublic:
    session.add(fake_todo)
    session.commit()

    session.refresh(fake_todo)

    return fake_todo


@pytest.fixture
def token(client: TestClient, user: User) -> str:
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.clean_password},
    )

    return response.json()["access_token"]
