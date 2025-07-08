from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import User, table_registry
from fastapi_zero.security import get_passaword_hash


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        echo=False,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()  # Fecha todas as conexoes do pool


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


@pytest.fixture
def users(session: Session):
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
    session.commit()
    session.refresh(user1)
    session.refresh(user2)
    user1.clean_password = password1
    return [user1, user2]


@pytest.fixture
def token(client, users):
    response = client.post(
        '/token',
        data={'username': users[0].email, 'password': users[0].clean_password},
    )
    return response.json()['access_token']
