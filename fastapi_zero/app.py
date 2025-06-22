from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='Minha Api Bala!')

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/html/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root_html():
    return """
    <html>
        <head>
            <title> Nosso olá mundo! </title>
        </head>
        <body>
            <h1>Olá Mundo</h1>
        </body>
    </html>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    """
    user_with_id = UserDB(
        username=user.username,
        email=user.email,
        password=user.password,
        id=len(database)+1
    )
    """
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.get(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_for_id(user_id: int):
    for data in database:
        if data.id == user_id:
            return data
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
    )


@app.put(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)

    for i in range(len(database)):
        if database[i].id == user_id:
            database[i] = user_with_id
            return user_with_id

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
    )


@app.delete(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    for data in database:
        if data.id == user_id:
            database.remove(data)
            return {'message': 'User Deleted!'}
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
    )
