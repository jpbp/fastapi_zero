from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_zero.security import get_current_user, get_passaword_hash

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session):
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


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: Session,
    current_user: CurrentUser,
    filter_users: Annotated[FilterPage, Query()],
):
    users = session.scalars(
        select(User).limit(filter_users.limit).offset(filter_users.offset)
    )
    return {'users': users}


@router.get(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_for_id(user_id: int, session: Session):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found!'
        )
    return user_db


@router.put(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    session: Session,
    current_user: CurrentUser,
    user_id: int,
    user: UserSchema,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not Enough permissions'
        )
    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_passaword_hash(user.password)
        session.commit()
        session.refresh(current_user)
        return current_user
    except IntegrityError:
        raise HTTPException(
            detail='Username or email already exists!',
            status_code=HTTPStatus.CONFLICT,
        )


@router.delete(
    '/{user_id}/', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(
    session: Session,
    current_user: CurrentUser,
    user_id: int,
):
    if current_user.id != user_id:
        raise HTTPException(
            detail='Not enough permission!', status_code=HTTPStatus.FORBIDDEN
        )
    session.delete(current_user)
    session.commit()
    return {'message': 'User Deleted!'}
