from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app
from fastapi_zero.schemas import UserPublic


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


def test_read_users(client, users, token):
    user1 = UserPublic.model_validate(users[0]).model_dump()
    user2 = UserPublic.model_validate(users[1]).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user1, user2]}


def test_read_user_with_id_valid(client, users):
    response = client.get(f'/users/{users[0].id}')
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


def test_update_user_with_id_valid(client, users, token):
    response = client.put(
        f'/users/{users[0].id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'ana-put',
            'email': 'ana-put@example.com',
            'password': 'senha-da-ana-put',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'ana-put',
        'email': 'ana-put@example.com',
        'id': 1,
    }


def test_update_user_integrity_error_email_exists(client, users, token):
    response = client.put(
        f'/users/{users[0].id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'jp',
            'email': 'teste@example.com',
            'password': 'senha-do-jp-put',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists!'}


def test_update_user_integrity_error_dunossaudo(client, users, token):
    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'senha-do-fausto',
        },
    )
    response = client.put(
        f'/users/{users[0].id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto-teste@example.com',
            'password': 'senha-do-fausto',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exists!'}


def test_update_user_forbidden(client, token):
    response = client.put(
        '/users/3',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'jp-teste',
            'email': 'jp-teste@example.com',
            'password': 'senha-do-jp-teste',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not Enough permissions'}


def test_delete_user_with_id_valid(client, users, token):
    response = client.delete(
        f'/users/{users[0].id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted!'}


def test_delete_user_with_id_UNAUTHORIZED(client, token):
    response = client.delete(
        '/users/3', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission!'}


def test_login_for_access_token_valid(client, users):
    response = client.post(
        '/token',
        data={'username': users[0].email, 'password': users[0].clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_login_for_access_token_invalid_email(client, users):
    response = client.post(
        '/token',
        data={'username': 'fake@email.com', 'password': 'senha123'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email'}


def test_login_for_access_token_invalid_password(client, users):
    response = client.post(
        '/token',
        data={'username': users[0].email, 'password': 'senha123'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect password'}
