from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from pydantic.alias_generators import to_snake
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from app.core.config import settings

engine = create_async_engine(str(settings.DATABASE_URL))
session_maker = async_sessionmaker(bind=engine)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


DatabaseSession = Annotated[AsyncSession, Depends(get_database_session)]


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return to_snake(cls.__name__)
