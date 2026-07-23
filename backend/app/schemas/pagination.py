from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]

    page: int
    page_size: int

    total: int
    total_pages: int

    has_next: bool
    has_previous: bool

    @classmethod
    def create(
        cls,
        items: list[T],
        page: int,
        page_size: int,
        total: int,
    ):
        total_pages = ceil(total / page_size) if total else 0

        return cls(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )