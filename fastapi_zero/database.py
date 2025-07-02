from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_zero.settings import Settings

engine = create_engine(
    Settings().DATABASE_URL,
    connect_args={'check_same_thread': False},
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


def get_session():
    with Session(engine) as session:
        yield session
