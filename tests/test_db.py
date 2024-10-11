from sqlalchemy import select

from fastzero.models import User


def test_create_user(session):
    user = User(username="schmidt", password="#123456", email="mail@mail.com")

    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(select(User).where(User.email == "mail@mail.com"))

    assert result.id == 1
    assert result.username == "schmidt"
