import asyncio

from http import HTTPStatus

import pytest

from ..testdata.schemas.person_schema import DetailPerson

from ..testdata import data_person

pytestmark = pytest.mark.asyncio


async def test_person_by_id(make_get_request):
    for person in data_person:
        person_id: str = person.get("id")
        # Выполнение запроса
        response = await make_get_request(endpoint=f"persons/{person_id}")
        response_body = response.body
        # Проверка результата Elastic
        assert response.status == HTTPStatus.OK
        assert DetailPerson(**response_body)
        assert response_body.get("uuid") == person_id
        assert response_body.get("full_name") == person.get("full_name")
        assert response_body.get("role") in person.get("roles")
        assert response_body.get("film_ids") == person.get("film_ids")


'''
async def test_person_films(make_get_request):
    test_person: dict = data_person[1]
    person_id: str = test_person.get("uuid")
    await asyncio.sleep(3)
    # Выполнение запроса
    response = await make_get_request(endpoint=f"persons/{person_id}/films/")
    response_body = response.body
    film_instances: list[dict] = [
        obj for obj in data_films if obj.get("id") in test_person.get("film_ids")
    ]
    # Проверка результата Elastic
    assert response.status == HTTPStatus.OK
    assert len(response_films) == len(film_instances)
    for response_film in response_films:
        for film_instance in film_instances:
            if film_instance.get("uuid") == response_film.get("uuid"):
                assert film_instance.get("id") == response_film.get("uuid")
                assert film_instance.get("title") == response_film.get("title")
                assert film_instance.get("imdb_rating") == response_film.get(
                    "imdb_rating"
                )
'''
