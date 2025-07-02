from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
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
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    # Verificar se username já existe
    db_user_username = session.scalar(
        select(User).where(User.username == user.username)
    )
    if db_user_username:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Username already exists!'
        )

    # Verificar se email já existe
    db_user_email = session.scalar(
        select(User).where(User.email == user.email)
    )
    if db_user_email:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists!'
        )

    # Criar novo usuário
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_for_id(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    return db_user


@app.put(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )

    put_user = UserDB(**user.model_dump(), id=user_id)
    db_user.username = put_user.username
    db_user.email = put_user.email
    db_user.password = put_user.password
    session.commit()
    return db_user


@app.delete(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    session.delete(db_user)
    session.commit()
    return {'message': 'User Deleted!'}
