from http import HTTPStatus


def test_created_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Titulo de exemplo',
            'description': 'Descrição de exemplo',
            'state': 'draft',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'Titulo de exemplo',
        'description': 'Descrição de exemplo',
        'state': 'draft',
        'id': 1,
    }


# def test_created_user_with_duplicated_email(client, other_user):
#     response = client.post(
#         '/users/',
#         json={
#             'username': 'ana-com-email-duplicado',
#             'email': other_user.email,
#             'password': 'senha-da-ana',
#         },
#     )
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Email already exists!'}


# def test_created_user_with_duplicated_username(client, other_user):
#     response = client.post(
#         '/users/',
#         json={
#             'username': other_user.username,
#             'email': 'ana@example.com',
#             'password': 'senha-da-ana',
#         },
#     )
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Username already exists!'}


# def test_created_user_fail_not_username(client):
#     response = client.post(
#         '/users', json={'email': 'user@example.com', 'password': 'string'}
#     )
#     assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT


# def test_read_users(client, user, other_user, token):
#     user = UserPublic.model_validate(user).model_dump()
#     other_user = UserPublic.model_validate(other_user).model_dump()
#     response = client.get(
#         '/users/', headers={'Authorization': f'Bearer {token}'}
#     )
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'users': [user, other_user]}


# def test_read_user_with_id_valid(client, user):
#     response = client.get(f'/users/{user.id}')
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'username': 'test10',
#         'email': 'test10@test.com',
#         'id': 1,
#     }


# def test_read_user_with_id_invalid(client):
#     response = client.get('/users/0')
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found!'}


# def test_update_user_with_id_valid(client, user, token):
#     response = client.put(
#         f'/users/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'test@test',
#             'email': 'testtest@test.com',
#             'password': 'senha-test',
#         },
#     )
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'username': 'test@test',
#         'email': 'testtest@test.com',
#         'id': 1,
#     }


# def test_update_user_integrity_error_email_exists(
#     client, user, other_user, token
# ):
#     response = client.put(
#         f'/users/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'test@test',
#             'email': other_user.email,
#             'password': 'senha-test',
#         },
#     )
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Username or email already exists!'}


# def test_update_user_integrity_error_dunossaudo(client, user, token):
#     response = client.post(
#         '/users/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'fausto',
#             'email': 'fausto@example.com',
#             'password': 'senha-do-fausto',
#         },
#     )
#     response = client.put(
#         f'/users/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'fausto',
#             'email': 'fausto-teste@example.com',
#             'password': 'senha-do-fausto',
#         },
#     )
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Username or email already exists!'}


# def test_update_user_forbidden(client, token, user, other_user):
#     response = client.put(
#         f'/users/{other_user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'jp-teste',
#             'email': 'jp-teste@example.com',
#             'password': 'senha-do-jp-teste',
#         },
#     )
#     assert response.status_code == HTTPStatus.FORBIDDEN
#     assert response.json() == {'detail': 'Not Enough permissions'}


# def test_update_user_with_wrong_user(client, user, other_user, token):
#     response = client.put(
#         f'/users/{other_user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'jp-teste',
#             'email': 'jp-teste@example.com',
#             'password': 'senha-do-jp-teste',
#         },
#     )
#     assert response.status_code == HTTPStatus.FORBIDDEN
#     assert response.json() == {'detail': 'Not Enough permissions'}


# def test_delete_user_with_id_valid(client, user, token):
#     response = client.delete(
#         f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
#     )
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'message': 'User Deleted!'}


# def test_delete_user_with_id_UNAUTHORIZED(client, other_user, token):
#     response = client.delete(
#         f'/users/{other_user.id}',
#           headers={'Authorization': f'Bearer {token}'}
#     )
#     assert response.status_code == HTTPStatus.FORBIDDEN
#     assert response.json() == {'detail': 'Not enough permission!'}
