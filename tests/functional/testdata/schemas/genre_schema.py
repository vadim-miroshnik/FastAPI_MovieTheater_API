from mixin import PaginationBase, UUIDBase


class FilmGenre(UUIDBase):

    name: str


class GenrePagination(PaginationBase):
    genres: list[FilmGenre] = []