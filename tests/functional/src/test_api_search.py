import asyncio
from http import HTTPStatus

import pytest

from ..schemas.movie_schema import FilmPagination
from ..schemas.person_schema import DetailPerson, PersonPagination
from ..settings import Settings
from ..testdata import data_films, person_data
from ..utils.hash_key_creater import create_hash_key

pytestmark = pytest.mark.asyncio


async def test_search_person(person_index, make_get_request, redis_cache):
    test_person: dict = person_data[1]
    query: str = "Jake"
    await asyncio.sleep(3)
    # Выполнение запроса
    response = await make_get_request(endpoint="persons/search", params={"query": query})
    response_body = response.body
    response_person: dict = response_body.get("persons")[0]
    # Проверка результата Elastic
    assert PersonPagination(**response_body)
    assert response.status == HTTPStatus.OK
    assert response_person.get("uuid") == test_person.get("id")
    assert response_person.get("full_name") == test_person.get("full_name")
    assert query in test_person.get("full_name")
    assert response_person.get("role") in test_person.get("roles")
    assert response_person.get("film_ids") == test_person.get("film_ids")
    # Проверка результата Redis
    page: int = response_body.get("page")
    page_size: int = response_body.get("page_size")
    total: int = response_body.get("total")
    key: str = create_hash_key(
        index=Settings.PERSON_INDEX, params=f"{total}{page}{page_size}{query}"
    )
    assert await redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None