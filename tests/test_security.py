from datetime import datetime, timedelta
from http import HTTPStatus

from jwt import decode, encode

from fastapi_zero.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)


def test_create_access_token():
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)
    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/3', headers={'Authorization': 'Bearer token-Invalido'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_token_without_sub(client):
    token_data = {
        'user_id': 123,
        'exp': datetime.utcnow()
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_token_invalid_email(client):
    token_data = {
        'sub': 'jp-fake@example.com',
        'user_id': 123,
        'exp': datetime.utcnow()
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
