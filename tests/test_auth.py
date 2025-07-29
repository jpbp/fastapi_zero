from http import HTTPStatus


def test_login_for_access_token_valid(client, users):
    response = client.post(
        '/auth/token',
        data={'username': users[0].email, 'password': users[0].clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_login_for_access_token_invalid_email(client, users):
    response = client.post(
        '/auth/token',
        data={'username': 'fake@email.com', 'password': 'senha123'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email'}


def test_login_for_access_token_invalid_password(client, users):
    response = client.post(
        '/auth/token',
        data={'username': users[0].email, 'password': 'senha123'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect password'}
