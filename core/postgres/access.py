from sqlalchemy.ext.asyncio import AsyncSession

from core.postgres.initialization import PostgresClient


async def get_async_session() -> AsyncSession:
    async_session_maker = PostgresClient.get_async_session()
    async with async_session_maker() as session:
        yield session
