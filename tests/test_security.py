from datetime import datetime, timedelta
from http import HTTPStatus

from jwt import decode, encode

from fastapi_zero.security import (
    create_access_token,
)


def test_create_access_token(settings):
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/3', headers={'Authorization': 'Bearer token-Invalido'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_token_without_sub(client, settings):
    token_data = {
        'user_id': 123,
        'exp': datetime.utcnow()
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = encode(
        token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# def test_get_current_user_token_invalid_email(client, settings):
#     token_data = {
#         'sub': 'jp-fake@example.com',
#         'user_id': 123,
#         'exp': datetime.utcnow()
#         + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
#     }
#     token = encode(
#         token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM
#     )

#     response = client.get(
#         '/users/', headers={'Authorization': f'Bearer {token}'}
#     )
#     print(response.status_code)
#     assert response.status_code == HTTPStatus.UNAUTHORIZED
#     assert response.json() == {'detail': 'Could not validate credentials'}
