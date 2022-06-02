from uuid import UUID
from typing import Optional
from models.base import BaseWithJsonModel


class Genre(BaseWithJsonModel):
    uuid: UUID
    name: str
    
class Person(BaseWithJsonModel):
    uuid: UUID
    full_name: str
    role: str
    film_ids: Optional[list[UUID]]
    

class Film(BaseWithJsonModel):
    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: Optional[list[str]]
    actors: Optional[list[Person]]
    writers: Optional[list[Person]]
    directors: Optional[list[Person]]    

class Films(BaseWithJsonModel):
    uuid: UUID
    title: str
    imdb_rating: float
