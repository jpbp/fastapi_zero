from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem tres etapas (AAA)
    A: Arrange - Arranjo (o que precisamos antes)
    A: Act - (aciona, faz com que a coisa que queremos testar SUT)
    A: Assert (garanta que A é A)
    """

    # arranjo
    client = TestClient(app)
    # act
    response = client.get('/')
    # assert
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK
