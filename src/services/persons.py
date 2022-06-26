from functools import lru_cache

from db.cache import AsyncCacheStorage
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.person import Person

from services.base_service import BaseService


class PersonService(BaseService):
    def __init__(self, cache: AsyncCacheStorage, elastic: AsyncElasticsearch):
        self.cache = cache
        self.elastic = elastic
        self.index = "persons"
        self.endpoint = "persons"
        self.etlmodel = Person


@lru_cache()
def get_person_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache, elastic)
