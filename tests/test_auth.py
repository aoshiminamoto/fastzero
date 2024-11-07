from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.clean_password},
    )

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_get_token_bad_request(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_token_inexistent_user(client):
    response = client.post(
        "/auth/token",
        data={"username": "no_user@no_domain.com", "password": "testtest"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect username or password"}


def test_token_wrong_password(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": "wrong_password"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Incorrect username or password"}


def test_token_expired_after_time(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.username, "password": user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.json()
        assert "token_type" in response.json()

        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "password": "wrong",
                "username": "wrongwrong",
                "email": "wrong@wrong.com",
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_refresh_token(client, user, token):
    response = client.post(
        "/auth/token/refresh",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data["token_type"] == "Bearer"
    assert "access_token" in data
    assert "token_type" in data


def test_token_expired_dont_refresh(client, user):
    with freeze_time("2023-07-14 12:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.username, "password": user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2023-07-14 12:31:00"):
        response = client.post(
            "/auth/token/refresh",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
