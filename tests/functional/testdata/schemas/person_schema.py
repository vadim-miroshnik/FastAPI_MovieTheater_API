from typing import Optional, List
from uuid import UUID

from ..schemas.mixin import PaginationBase, UUIDBase


class FilmPerson(UUIDBase):

    full_name: str


class DetailPerson(FilmPerson):

    role: str
    film_ids: Optional[List[UUID]] = []


class PersonPagination(PaginationBase):
    persons: List[DetailPerson] = []