from typing import List

from ..schemas.mixin import PaginationBase, UUIDBase


class FilmGenre(UUIDBase):

    name: str


class GenrePagination(PaginationBase):
    genres: List[FilmGenre] = []