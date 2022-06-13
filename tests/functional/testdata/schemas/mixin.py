from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UUIDBase(BaseModel):
    uuid: UUID


class PaginationBase(BaseModel):
    total: int
    page: int
    page_size: int
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    available_pages: list