from typing import Optional
from uuid import UUID

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from models.base import BaseWithJsonModel

class Genre(BaseWithJsonModel):
    id: UUID
    name: str


class Person(BaseWithJsonModel):
    id: UUID
    name: str


class Film(BaseWithJsonModel):
    id: UUID
    title: str
    imdb_rating: float
    description: str
    genre: Optional[list[str]]
    actors: Optional[list[Person]]
    writers: Optional[list[Person]]
    directors: Optional[list[Person]]

class PersonFull(Person, BaseWithJsonModel):
    role: str
    film_ids: Optional[list[str]]
