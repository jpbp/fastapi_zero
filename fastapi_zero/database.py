from sqlalchemy.ext import create_async_engine, AsyncSession
from sqlalchemy.orm import Session

from fastapi_zero.settings import Settings

engine = create_async_engine(
    Settings().DATABASE_URL,
    connect_args={'check_same_thread': False},
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
