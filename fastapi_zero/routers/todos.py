from http import HTTPStatus, HTTPException
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import Todo, User
from fastapi_zero.schemas import FilterTodo, TodoList, TodoPublic, TodoSchema, Message
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
async def list_todos(
    session: Session,
    user: CurrentUser,
    filter_todos: Annotated[FilterTodo, Query()],
):
    query = select(Todo).where(Todo.user_id == user.id)

    if filter_todos.title:
        query = query.filter(Todo.title.contains(filter_todos.title))

    if filter_todos.description:
        query = query.filter(
            Todo.description.contains(filter_todos.description)
        )

    if filter_todos.state:
        query = query.filter(Todo.state == filter_todos.state)

    todos = await session.scalars(
        query.offset(filter_todos.offset).limit(filter_todos.limit)
    )
    return {'todos': todos}


@router.delete('/{todo_id}',status_code=HTTPStatus.OK,response_model=Message)
async def delete_todo(
    session: Session,
    user: CurrentUser,
    todo_id: int
):
    todo = await session.scalar(
        select(Todo)
        .where(
            Todo.user_id == user.id , Todo.id == todo_id)
        )
    
    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )
    session.delete(todo)
    await session.commit()
    return {'message': 'Task has been deleted successfuly'}
    
    