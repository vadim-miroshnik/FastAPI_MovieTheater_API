from functools import lru_cache

from db.cache import AsyncCacheStorage
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film

from services.base_service import BaseService


class FilmService(BaseService):
    def __init__(self, cache: AsyncCacheStorage, elastic: AsyncElasticsearch):
        self.cache = cache
        self.elastic = elastic
        self.index = "movies"
        self.endpoint = "movies"
        self.etlmodel = Film


@lru_cache()
def get_film_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache, elastic)
