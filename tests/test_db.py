from sqlalchemy import select

from fastzero.models import Todo, User


def test_create_user(session):
    user = User(username="schmidt", password="#123456", email="mail@mail.com")

    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(select(User).where(User.email == "mail@mail.com"))

    assert result.id == 1
    assert result.username == "schmidt"


def test_create_todo(session, user: User):
    todo = Todo(
        state="draft",
        user_id=user.id,
        title="Test Todo",
        description="Test Desc",
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
