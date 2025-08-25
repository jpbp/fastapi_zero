from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import Todo, User
from fastapi_zero.schemas import FilterPage, TodoList, TodoPublic, TodoSchema
from fastapi_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['TODOS'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TodoPublic)
async def create_todo(todo: TodoSchema, session: Session, user: CurrentUser):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo


@router.get('/', status_code=HTTPStatus.OK, response_model=TodoList)
async def get_todo(
    session: Session,
    user: CurrentUser,
    filter_todos: Annotated[FilterPage, Query()],
):
    todos = await session.scalars(
        select(Todo)
        .join(User)
        .where(User.id == user.id)
        .limit(filter_todos.limit)
        .offset(filter_todos.offset)
    )
    return {'todos': todos}
