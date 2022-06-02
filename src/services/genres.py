from functools import lru_cache
import json
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis, get_redis_data, set_redis_data
from models.genre import Genre
from core.utils import make_cache_key

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genres_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre
    
    async def get_persons(self, search_query: str, page: int, sort: Optional[str], ):
        films = await self._get_genres_from_elastic(search_query=search_query,sort=sort,filter=filter,page=page)
        return films

    async def _get_genres_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])
    
    async def get_all_genres(self, search_query: str, page: int, sort: Optional[str], ):
        genres = await self._get_all_genres_from_cache(search_query=search_query, sort=sort, filter=filter, page=page)
        if not genres:
            genres = await self._get_all_genres_from_elastic(search_query=search_query,sort=sort,filter=filter,page=page)
            if not genres:
                return None
            await self._put_all_genres_to_cache(genres=genres,search_query=search_query,sort=sort,filter=filter,page=page)
        return genres

    
    async def _get_all_genres_from_elastic(
            self,
            search_query: Optional[str],
            sort: Optional[str],
            filter: Optional[dict],
            page: dict):
        body = {
            "query": {
                "bool": {
                    "must": []
                }}}

        if search_query is not None:
            body["query"]["bool"]["must"].append(
                {"match": {"title": str(search_query)}}
            )
        if filter is None and search_query is None:
            body = None
        response = await self.elastic.search(
            index="genres",
            from_=(page["number"] - 1) * page["size"],
            size=page["size"],
            request_timeout=5,
            sort=sort,
            body=body,
        )
        return response

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        key = make_cache_key(endpoint="genre",id=str(genre_id))
        data = await self.redis.get(key)
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        key = make_cache_key(endpoint="genre",id=str(genre.id))
        value = genre.json()
        await self.redis.set(key = key, value = value, expire=GENRE_CACHE_EXPIRE_IN_SECONDS)


    async def _get_all_genres_from_cache(
            self,
            search_query: Optional[str],
            sort: Optional[str],
            filter: Optional[dict],
            page: dict):

        key=make_cache_key(endpoint="genres",
                search_query=search_query,
                sort=sort,
                filter=filter,
                page=page)
        data = await self.redis.get(key)
        if not data:
            return None
        genres= json.loads(data)
        return genres

    async def _put_all_genres_to_cache(
            self,
            genres,
            search_query: Optional[str],
            sort: Optional[str],
            filter: Optional[dict],
            page: dict):

        key = make_cache_key(
            endpoint="genres",
            search_query=search_query,
            sort=sort,
            filter=filter,
            page=page,
        )
        value = json.dumps(genres)
        await self.redis.set(key = key, value = value, expire=GENRE_CACHE_EXPIRE_IN_SECONDS)  

    
@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)