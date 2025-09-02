from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem tres etapas (AAA)
    A: Arrange - Arranjo (o que precisamos antes)
    A: Act - (aciona, faz com que a coisa que queremos testar SUT)
    A: Assert (garanta que A é A)
    """

    # act
    response = client.get('/')
    # assert
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_read_root_html_retornar_ola_mundo_html(client):
    # act
    response = client.get('/html')
    # assert
    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'].startswith('text/html')
    assert '<h1>Olá Mundo</h1>' in response.text
    assert '<title> Nosso olá mundo! </title>' in response.text


def test_read_root_html_content_type():
    client = TestClient(app)
    response = client.get('/html')
    assert response.headers['content-type'].startswith('text/html')


def test_healthcheck(client):
    """
    Esse teste tem tres etapas (AAA)
    A: Arrange - Arranjo (o que precisamos antes)
    A: Act - (aciona, faz com que a coisa que queremos testar SUT)
    A: Assert (garanta que A é A)
    """

    # act
    response = client.get('/healthcheck')
    # assert
    assert response.json() == {'message': 'Health - OK'}
    assert response.status_code == HTTPStatus.OK
