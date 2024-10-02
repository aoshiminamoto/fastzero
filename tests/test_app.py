from http import HTTPStatus

from fastapi.testclient import TestClient

from fastzero.app import app


def test_read_root_statuscode_e_ola_mundo():
    client = TestClient(app)  # Arrange (Organização)
    response = client.get("/")  # Actt (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)

    assert response.json() == "Batatinhas Fritas Voadoras"
