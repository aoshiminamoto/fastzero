from http import HTTPStatus


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


def test_read_user(client):
    responde = client.get("/users/")

    assert responde.status_code == HTTPStatus.OK

    assert responde.json() == {
        "users": [
            {
                "username": "joaozinho",
                "email": "J@test.com",
                "id": 1,
            }
        ]
    }


def test_read_user_by_id(client):
    responde = client.get("/users/1")

    assert responde.status_code == HTTPStatus.OK

    assert responde.json() == {
        "username": "joaozinho",
        "email": "J@test.com",
        "id": 1,
    }


def test_read_user_by_id_error404(client):
    response = client.get("/users/0")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "joaozinho",
            "email": "J@test.com",
            "password": "#1234",
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        "username": "joaozinho",
        "email": "J@test.com",
        "id": 1,
    }


def test_update_user_error404(client):
    response = client.put(
        "/users/0",
        json={
            "username": "joaozinho",
            "email": "J@test.com",
            "password": "#1234",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {"message": "User deleted!"}


def test_delete_user_error404(client):
    response = client.delete("/users/0")

    assert response.status_code == HTTPStatus.NOT_FOUND
