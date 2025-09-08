from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_db_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test', email='test@test.com', password='secret'
        )
        session.add(new_user)
        await session.commit()
        user = await session.scalar(
            select(User).where(User.username == 'test')
        )
        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test.com',
            'password': 'secret',
            'todos': [],
            'created_at': time,
            'updated_at': time,
        }


@pytest.mark.asyncio
async def test_create_db_todo(session: AsyncSession, mock_db_time, user):
    with mock_db_time(model=Todo) as time:
        new_todo = Todo(
            description='teste', state='doing', title='teste', user_id=user.id
        )
        session.add(new_todo)
        await session.commit()
        todo = await session.scalar(
            select(Todo).where(Todo.description == 'teste')
        )
        assert asdict(todo) == {
            'id': 1,
            'description': 'teste',
            'title': 'teste',
            'state': 'doing',
            'created_at': time,
            'updated_at': time,
            'user_id': user.id,
        }


@pytest.mark.asyncio
async def test_enum_invalido(session: AsyncSession, user):
    """Garante que um valor inválido no Enum de Todo gera erro.

    Para colunas Enum do SQLAlchemy, um valor inválido é validado no
    bind/flush e a exceção propagada é um StatementError contendo a
    mensagem "not among the defined enum values" (a causa original é
    um LookupError interno do SQLAlchemy).
    """
    new_todo = Todo(
        description='teste',
        state='batatinha',  # inválido para TodoState
        title='teste',
        user_id=user.id,
    )
    session.add(new_todo)
    await session.commit()
    with pytest.raises(LookupError):
        await session.scalar(select(Todo).where(Todo.description == 'teste'))

    await session.flush()
