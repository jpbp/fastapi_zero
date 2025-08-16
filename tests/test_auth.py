from http import HTTPStatus

from freezegun import freeze_time


def test_login_for_access_token_valid(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_login_for_access_token_invalid_email(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'fake@email.com', 'password': 'senha123'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email'}


def test_login_for_access_token_invalid_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'senha123'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect password'}


def test_token_expired_after_time(client, user):
    with freeze_time('2025-12-31 12:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-12-31 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrong',
                'email': 'wrong@wrong.com',
                'password': 'wrongpass',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, user, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    token_refreshed = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token_refreshed
    assert token_refreshed['token_type'] == 'Bearer'


def test_refresh_token_expired_after_time(client, user):
    with freeze_time('2025-12-31 12:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        token = response.json()['access_token']

    with freeze_time('2025-12-31 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
