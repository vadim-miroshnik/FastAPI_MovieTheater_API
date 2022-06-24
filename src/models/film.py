from typing import List, Optional
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
    genre: Optional[List[str]]
    actors: Optional[List[Person]]
    writers: Optional[List[Person]]
    directors: Optional[List[Person]]


class PersonFull(Person, BaseWithJsonModel):
    role: str
    film_ids: Optional[List[str]]
