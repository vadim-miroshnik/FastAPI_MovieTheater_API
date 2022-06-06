from typing import Optional, List
from uuid import UUID

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from models.base import BaseWithJsonModel

class Person(BaseWithJsonModel):
    id: str
    full_name: str
    role: str
    film_ids: Optional[List[UUID]]