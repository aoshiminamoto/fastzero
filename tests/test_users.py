from http import HTTPStatus

from fastzero.schemas import UserPublic
from fastzero.security import create_access_token


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "joaozinho",
            "email": "J@test.com",
            "password": "#1234",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        "username": "joaozinho",
        "email": "J@test.com",
        "id": 1,
    }


def test_create_user_username_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "J@test.com",
            "password": "#1234",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_email_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "josejoaozinho",
            "email": user.email,
            "password": "#1234",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_read_user(client, user, token):
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [UserPublic.model_validate(user).model_dump()]
    }


def test_read_user_by_id(client, user, token):
    response = client.get(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == UserPublic.model_validate(user).model_dump()


def test_read_user_by_id_not_found(client, token):
    response = client.get(
        "/users/0",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        json={
            "password": "#1234",
            "email": "J@test.com",
            "username": "joaozinho",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == UserPublic.model_validate(user).model_dump()


def test_update_user_forbidden(client, other_user, token):
    response = client.put(
        f"/users/{other_user.id}",
        json={
            "password": "#1234",
            "email": "J@test.com",
            "username": "joaozinho",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_forbidden(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_get_current_user_not_found(client):
    token = create_access_token({"no-email": "test"})

    response = client.delete(
        "/users/0",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_get_current_user_does_not_exists(client):
    token = create_access_token({"sub": "test@test"})

    response = client.delete(
        "/users/0",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
