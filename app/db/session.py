from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import get_settings

global_settings = get_settings()


# Engines
engine = create_engine(global_settings.POSTGRES_URL)
test_engine = create_engine(global_settings.POSTGRES_TEST_URL)

# Sessions
session = scoped_session(sessionmaker(bind=engine))
test_session = scoped_session(sessionmaker(bind=test_engine))

# Main DB
async_session_maker = sessionmaker(
    bind=create_async_engine(global_settings.POSTGRES_ASYNC_URL),
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
