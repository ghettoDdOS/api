from fastapi import UploadFile
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, DatabaseSession
from app.core.models import BaseModel
from app.core.types import FSSpecField


class UserModel(Base):
    email: Mapped[str] = mapped_column(unique=True)
    avatar: Mapped[str | None] = mapped_column(
        FSSpecField(upload_to='users/avatars/%d/')
    )


class User(BaseModel):
    id: int
    email: EmailStr
    avatar: str | None = None


class BaseRepository[T: Base]:
    def __init__(self, model: T, session: AsyncSession) -> None:
        self.model = model
        self.session = session

    def get(self) -> T:
        return self.model


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: DatabaseSession) -> None:
        self.db = db


class UserCreate(BaseModel):
    email: EmailStr
    avatar: UploadFile | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    avatar: UploadFile | None = None
