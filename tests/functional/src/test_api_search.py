import asyncio

from http import HTTPStatus

import pytest

from ..testdata.schemas.person_schema import DetailPerson

from ..testdata import data_films, data_person

pytestmark = pytest.mark.asyncio


async def test_search_person(make_get_request):
    test_person: dict = data_person[0]
    query: str = test_person.get("full_name") #"Jake"
    await asyncio.sleep(3)
    # Выполнение запроса
    response = await make_get_request(endpoint="persons/search/", params={"query": query})
    response_body = response.body
    response_person: dict = response_body[0]
    # Проверка результата Elastic
    assert response.status == HTTPStatus.OK
    assert response_person.get("uuid") == test_person.get("id")
    assert response_person.get("full_name") == test_person.get("full_name")
    assert query in test_person.get("full_name")
    assert response_person.get("role") in test_person.get("roles")
    assert response_person.get("film_ids") == test_person.get("film_ids")
