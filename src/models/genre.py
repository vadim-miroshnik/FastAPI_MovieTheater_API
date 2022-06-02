from uuid import UUID

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from models.base import BaseWithJsonModel

class Genre(BaseWithJsonModel):
    id: UUID
    name: str