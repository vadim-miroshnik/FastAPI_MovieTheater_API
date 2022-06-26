from functools import lru_cache

from db.cache import AsyncCacheStorage
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.genre import Genre

from services.base_service import BaseService


class GenreService(BaseService):
    def __init__(self, cache: AsyncCacheStorage, elastic: AsyncElasticsearch):
        self.cache = cache
        self.elastic = elastic
        self.index = "genres"
        self.endpoint = "genres"
        self.etlmodel = Genre


@lru_cache()
def get_genre_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, elastic)
