from typing import Optional, List

from ..schemas.mixin import PaginationBase, UUIDBase
from ..schemas.genre_schema import FilmGenre
from ..schemas.person_schema import FilmPerson


class ListFilm(UUIDBase):

    title: str
    imdb_rating: Optional[float] = None


class DetailResponseFilm(ListFilm):

    description: Optional[str] = None
    genre: Optional[List[FilmGenre]] = []
    actors: Optional[List[FilmPerson]] = []
    writers: Optional[List[FilmPerson]] = []
    directors: Optional[List[FilmPerson]] = []


class FilmPagination(PaginationBase):
    films: List[ListFilm] = []
