from typing import Optional

from genre_schema import FilmGenre
from mixin import PaginationBase, UUIDBase
from person_schema import FilmPerson


class ListFilm(UUIDBase):

    title: str
    imdb_rating: Optional[float] = None


class DetailResponseFilm(ListFilm):

    description: Optional[str] = None
    genre: Optional[list[FilmGenre]] = []
    actors: Optional[list[FilmPerson]] = []
    writers: Optional[list[FilmPerson]] = []
    directors: Optional[list[FilmPerson]] = []


class FilmPagination(PaginationBase):
    films: list[ListFilm] = []
