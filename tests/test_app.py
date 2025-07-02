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


def test_created_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'ana',
            'email': 'ana@example.com',
            'password': 'senha-da-ana',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'ana',
        'email': 'ana@example.com',
        'id': 1,
    }


def test_created_user_with_duplicated_email(client):
    response = client.post(
        '/users/',
        json={
            'username': 'ana',
            'email': 'ana@example.com',
            'password': 'senha-da-ana',
        },
    )
    response = client.post(
        '/users/',
        json={
            'username': 'ana-com-email-duplicado',
            'email': 'ana@example.com',
            'password': 'senha-da-ana',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists!'}


def test_created_user_with_duplicated_username(client):
    response = client.post(
        '/users/',
        json={
            'username': 'ana',
            'email': 'ana@example.com',
            'password': 'senha-da-ana',
        },
    )
    response = client.post(
        '/users/',
        json={
            'username': 'ana',
            'email': 'ana-com-username-duplicado@example.com',
            'password': 'senha-da-ana',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists!'}


def test_created_user_fail_not_username(client):
    response = client.post(
        '/users', json={'email': 'user@example.com', 'password': 'string'}
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


def test_read_users(client, users):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'username': 'ana', 'email': 'ana@example.com', 'id': 1},
            {'username': 'jp', 'email': 'jp@example.com', 'id': 2},
        ]
    }


def test_read_users_empty(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_with_id_valid(client, users):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'ana',
        'email': 'ana@example.com',
        'id': 1,
    }


def test_read_user_with_id_invalid(client, users):
    response = client.get('/users/3')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_update_user_with_id_valid(client, users):
    response = client.put(
        '/users/2',
        json={
            'username': 'jp-put',
            'email': 'jp-put@example.com',
            'password': 'senha-do-jp-put',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'jp-put',
        'email': 'jp-put@example.com',
        'id': 2,
    }


def test_update_user_with_id_invalid(client, users):
    response = client.put(
        '/users/3',
        json={
            'username': 'jp-teste',
            'email': 'jp-teste@example.com',
            'password': 'senha-do-jp-teste',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_delete_user_with_id_valid(client, users):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted!'}
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted!'}


def test_delete_user_with_id_invalid(client, users):
    response = client.delete('/users/3')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
