import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.logger import logger
from core.postgres.__all_models import load_all_models
from core.settings import settings


# Класс для создания таблиц
class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow(),
    )

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


# Инициализация Postgres
class PostgresClient:
    _engine: AsyncEngine | None = None
    _async_session_maker: async_sessionmaker | None = None

    @classmethod
    async def init_postgres(cls) -> None:
        if cls._async_session_maker is not None:
            logger.error("Postgres is already initialized")
            return

        cls._engine = create_async_engine(settings.get_postgres_url(), max_overflow=1100, pool_size=1000)
        cls._async_session_maker = async_sessionmaker(bind=cls._engine, expire_on_commit=False)

        load_all_models(["services.objects.models", "services.reports.models"])

        async with cls._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Postgres initialized")

    @classmethod
    async def close_postgres(cls) -> None:
        if cls._engine is not None:
            logger.info("Postgres closed")
            await cls._engine.dispose()
            cls._engine = None
            cls._async_session_maker = None

    @classmethod
    def get_async_session(cls) -> async_sessionmaker:
        return cls._async_session_maker
