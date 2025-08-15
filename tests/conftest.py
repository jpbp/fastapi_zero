from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry
from fastapi_zero.security import get_passaword_hash
from fastapi_zero.settings import Settings


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(model, time=datetime(2025, 5, 20)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at') and hasattr(target, 'updated_at'):
            target.created_at = time
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def users(session: AsyncSession):
    password1 = 'senha-da-ana'
    user1 = User(
        username='ana',
        email='ana@example.com',
        password=get_passaword_hash(password1),
    )
    user2 = User(
        username='jp',
        email='jp@example.com',
        password=get_passaword_hash('senha-do-jp'),
    )
    session.add(user1)
    session.add(user2)
    await session.commit()
    await session.refresh(user1)
    await session.refresh(user2)
    user1.clean_password = password1
    return [user1, user2]


@pytest.fixture
def token(client, users):
    response = client.post(
        '/auth/token',
        data={'username': users[0].email, 'password': users[0].clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()
