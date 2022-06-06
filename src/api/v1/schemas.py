from uuid import UUID
from typing import Optional, List
from models.base import BaseWithJsonModel


class Genre(BaseWithJsonModel):
    uuid: UUID
    name: str
    
class Person(BaseWithJsonModel):
    uuid: UUID
    full_name: str
    role: str
    film_ids: Optional[List[UUID]]
    
class FilmPerson(BaseWithJsonModel):
    uuid: UUID
    full_name: str

class Film(BaseWithJsonModel):
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: Optional[List[str]]
    actors: Optional[List[FilmPerson]]
    writers: Optional[List[FilmPerson]]
    directors: Optional[List[FilmPerson]]    
    
class Films(BaseWithJsonModel):
    uuid: UUID
    title: str
    imdb_rating: float
