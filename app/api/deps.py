from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel


class PaginatedResponse[T](BaseModel):
    results: list[T]


class LimitOffset(BaseModel):
    limit: int
    offset: int


def provide_limit_offset_pagination(
    limit: int = 20,
    offset: int = 0,
) -> LimitOffset:
    return LimitOffset(limit=limit, offset=offset)


LimitOffsetPagination = Annotated[
    LimitOffset, Depends(provide_limit_offset_pagination)
]
