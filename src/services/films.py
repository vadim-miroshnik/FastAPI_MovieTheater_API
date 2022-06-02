from functools import lru_cache
import json
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_scan
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from core.utils import make_cache_key

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film = await self._get_film_from_elastic(film_id)
            if not film:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        key = make_cache_key(endpoint="film",id=str(film_id))
        data = await self.redis.get(key)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        key = make_cache_key(endpoint="film",id=str(film.id))
        value = film.json()
        await self.redis.set(key = key, value = value, expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def get_films(self, search_query: Optional[str], person_id: Optional[str], sort: Optional[str], filter: Optional[dict],page: dict):
        films = await self._get_films_from_cache(search_query=search_query, sort=sort, filter=filter, page=page)
        if not films:
            films = await self._get_films_from_elastic(search_query=search_query,person_id=person_id, sort=sort,filter=filter,page=page)
            if not films:
                return None
            await self._put_films_to_cache(films=films,search_query=search_query,sort=sort,filter=filter,page=page)
        return films
    

    async def _get_films_from_elastic(
            self,
            search_query: Optional[str],
            person_id: Optional[str],
            sort: Optional[str],
            filter: Optional[dict],
            page: dict):
        body = {
            "query": {
                "bool": {
                    "must": []
                }}}
        if filter is not None:

            if type(filter.get("genre")) is str:
                filter["genre"] = [filter.get("genre"), ]
            
                for genre_id in filter.get("genre"):
                    body["query"]["bool"]["must"].append(
                        {"nested": {"path": "genre", "query": {"match": {"genre.id": str(genre_id)}}}}
                    )
        
            elif type(filter.get("person")) is str:
                for field_name in ("directors", "actors", "writers"):
                    filter[field_name] = [filter.get(field_name), ]
                    body["query"]["bool"]["must"].append(
                        {"nested": {"path": field_name, "query": {"match": {f"{field_name}.id": str(person_id)}}}}
                    )


        if search_query is not None:
            body["query"]["bool"]["must"].append(
                {"match": {"title": str(search_query)}}
            )
        if filter is None and search_query is None:
            body = None
        response = await self.elastic.search(
            index="movies",
            from_=(page["number"] - 1) * page["size"],
            size=page["size"],
            request_timeout=5,
            sort=sort,
            body=body,
        )

        return response
    
    async def get(self, id_: str):
        response = await self.elastic.get(index=self.index, id=id_)
        return self.model(**response['_source'])

    async def _get_films_from_cache(
            self,
            search_query: Optional[str],
            sort: Optional[str],
            filter: Optional[dict],
            page: dict):

        key=make_cache_key(endpoint="films",
                search_query=search_query,
                sort=sort,
                filter=filter,
                page=page)
        data = await self.redis.get(key)
        if not data:
            return None
        films= json.loads(data)
        return films

    async def _put_films_to_cache(
            self,
            films,
            search_query: Optional[str],
            sort: Optional[str],
            filter: Optional[dict],
            page: dict):

        key = make_cache_key(
            endpoint="films",
            search_query=search_query,
            sort=sort,
            filter=filter,
            page=page,
        )
        value = json.dumps(films)
        await self.redis.set(key = key, value = value, expire=FILM_CACHE_EXPIRE_IN_SECONDS)  


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
