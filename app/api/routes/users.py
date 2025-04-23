from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status
from sqlalchemy import select

from app.api.deps import LimitOffsetPagination, PaginatedResponse
from app.core.db import DatabaseSession
from app.models import User, UserCreate, UserModel, UserUpdate

router = APIRouter(tags=['users'])

base_path = '/users/'
detail_path = base_path + '{user_id}'


@router.get(base_path, response_model=PaginatedResponse[User])
async def list_users(
    limit_offset: LimitOffsetPagination,
) -> None:
    pass


@router.post(
    base_path,
    response_model=User,
)
async def create_user(
    db: DatabaseSession,
    data: Annotated[UserCreate, Form(media_type='multipart/form-data')],
) -> UserModel:
    obj = UserModel(email=data.email, avatar=data.avatar)
    async with db.begin():
        db.add(obj)
    return obj


@router.get(detail_path, response_model=User)
async def get_user(db: DatabaseSession, user_id: int) -> UserModel:
    query = select(UserModel).where(UserModel.id == user_id)
    obj = await db.execute(query)
    obj = obj.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f'User with id: {user_id} not found'
        )
    return obj


@router.patch(detail_path, response_model=User)
async def update_user(data: UserUpdate, user_id: int) -> None:
    pass


@router.delete(detail_path)
async def delete_user(user_id: int) -> None:
    pass
