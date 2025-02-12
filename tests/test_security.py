from http import HTTPStatus

from jwt import decode

from fastzero.security import create_access_token, settings


def test_jwt():
    data = {"sub": "test@test.com"}
    token = create_access_token(data)
    decoded = decode(token, settings.SECRET_KEY, [settings.ALGORITHM])

    assert decoded["exp"]
    assert decoded["sub"] == data["sub"]


def test_jwt_invalid_token(client):
    response = client.delete("/users/1", headers={"Authorization": "Bearer token-invalido"})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
