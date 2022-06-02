from functools import lru_cache
import json
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis, get_redis_data, set_redis_data
from models.person import Person
from core.utils import make_cache_key

PERSONS_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут




class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:

        person = await self._get_person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None

            await self._put_person_to_cache(person)

        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def _get_person_from_cache(self, person_id: str) -> Optional[Person]:
        key = make_cache_key(endpoint="person",id=str(person_id))
        data = await self.redis.get(key)
        if not data:
            return None

        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: Person):
        key = make_cache_key(endpoint="person",id=str(person.id))
        value = person.json()
        await self.redis.set(key = key, value = value, expire=PERSONS_CACHE_EXPIRE_IN_SECONDS)

    async def _get_person_all_role(self, person_id: str) -> dict[str, list[str]]:
        
        ids_films_writer = await self._get_role_films(person_id=person_id, role='writers')
        ids_films_director = await self._get_role_films(person_id=person_id, role='directors')
        ids_films_actor = await self._get_role_films(person_id=person_id, role='actors')

        role_list = {
            'writer': ids_films_writer,
            'director': ids_films_director,
            'actor': ids_films_actor
        }
        return role_list
    
    async def _get_role_films(self, person_id: str, role: str) -> list:
        body = {
            'query': {
                'bool': {
                    'filter': {
                        'nested': {
                            'path': role,
                            'query': {
                                'bool': {
                                    'filter': {
                                        'term': {role + '.id': person_id}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        ids_films = await self.search_role_ids(body=body)
        return ids_films

    async def search_role_ids(self, body: dict):
        doc = await self.elastic.search(index='movies', body=body, size=999)
        ids_films = [x['_source']['id'] for x in doc['hits']['hits']]
        return ids_films
    
    async def get_persons(self, search_query: str, page: int, sort: Optional[str], ):
        persons = await self._get_persons_from_cache(search_query=search_query, sort=sort, filter=filter, page=page)
        if not persons:
            persons = await self._get_persons_from_elastic(search_query=search_query,sort=sort,filter=filter,page=page)
            if not persons:
                return None
            await self._put_persons_to_cache(persons=persons,search_query=search_query,sort=sort,filter=filter,page=page)
        return persons    

    async def _get_persons_from_elastic(
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
                {"match": {"full_name": str(search_query)}}
            )
        if filter is None and search_query is None:
            body = None
        response = await self.elastic.search(
            index="persons",
            from_=(page["number"] - 1) * page["size"],
            size=page["size"],
            request_timeout=5,
            sort=sort,
            body=body,
        )
        return response

    async def _get_persons_from_cache(
            self,
            search_query: Optional[str],
            sort: Optional[str],
            filter: Optional[dict],
            page: dict):

        key=make_cache_key(endpoint="persons",
                search_query=search_query,
                sort=sort,
                filter=filter,
                page=page)
        data = await self.redis.get(key)
        if not data:
            return None
        persons= json.loads(data)
        return persons

    async def _put_persons_to_cache(
            self,
            persons,
            search_query: Optional[str],
            sort: Optional[str],
            filter: Optional[dict],
            page: dict):

        key = make_cache_key(
            endpoint="persons",
            search_query=search_query,
            sort=sort,
            filter=filter,
            page=page,
        )
        value = json.dumps(persons)
        await self.redis.set(key = key, value = value, expire=PERSONS_CACHE_EXPIRE_IN_SECONDS)

@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
