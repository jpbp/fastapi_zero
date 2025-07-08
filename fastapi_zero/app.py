from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    Message,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_zero.security import (
    create_access_token,
    get_current_user,
    get_passaword_hash,
    verify_password,
)

app = FastAPI(title='Minha Api Bala!')


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
    user_db_username = session.scalar(
        select(User).where(User.username == user.username)
    )
    if user_db_username:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Username already exists!'
        )

    # Verificar se email já existe
    user_db_email = session.scalar(
        select(User).where(User.email == user.email)
    )
    if user_db_email:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists!'
        )

    # Criar novo usuário
    user_db = User(
        username=user.username,
        email=user.email,
        password=get_passaword_hash(user.password),
    )
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_for_id(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    return user_db


@app.put(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, 
    user: UserSchema, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    existingUser = session.scalar(
        select(User).where(
            (
                and_(
                    User.id != user_db.id,
                    or_(
                        User.username == user.username,
                        User.email == user.email,
                    ),
                )
            )
        )
    )
    if not existingUser:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = get_passaword_hash(user.password)
        session.commit()
        session.refresh(user_db)
        return user_db
    elif existingUser.username == user.username:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username already exists!',
        )
    elif existingUser.email == user.email:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists!'
        )


@app.delete(
    '/users/{user_id}/', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    session.delete(user_db)
    session.commit()
    return {'message': 'User Deleted!'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email',
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect password',
        )

    access_token = create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}
