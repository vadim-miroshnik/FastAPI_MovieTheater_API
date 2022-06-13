from typing import Optional
from uuid import UUID

from mixin import PaginationBase, UUIDBase


class FilmPerson(UUIDBase):

    full_name: str


class DetailPerson(FilmPerson):

    role: str
    film_ids: Optional[list[UUID]] = []


class PersonPagination(PaginationBase):
    persons: list[DetailPerson] = []