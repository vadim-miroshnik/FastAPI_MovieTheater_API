import asyncio
from http import HTTPStatus

import pytest

from ..testdata import data_genre
from ..testdata.schemas.genre_schema import FilmGenre

pytestmark = pytest.mark.asyncio


async def test_genre_by_id(make_get_request):
    for test_genre in data_genre:
        genre_id: str = test_genre.get("uuid")
        # Выполнение запроса
        response = await make_get_request(endpoint=f"genres/{genre_id}")
        response_body = response.body
        # Проверка результата Elastic
        assert response.status == HTTPStatus.OK
        assert FilmGenre(**response_body)
        assert test_genre.get("uuid") == response_body.get("uuid")
        assert test_genre.get("name") == response_body.get("name")


async def test_genres_list(make_get_request):
    await asyncio.sleep(3)
    # Выполнение запроса
    response = await make_get_request(endpoint="genres/")
    response_body = response.body
    # response_genres = response_body.get("genres")
    # Проверка результата Elastic
    assert response.status == HTTPStatus.OK
    assert len(response_body) == len(data_genre)
    for genre in data_genre:
        for response_genre in response_body:
            if genre["uuid"] == response_genre["uuid"]:
                assert genre.get("uuid") == response_genre.get("uuid")
                assert genre.get("name") == response_genre.get("name")


@pytest.mark.asyncio
async def test_genre_by_wrong_id(make_get_request):
    genre_id = "11111111-c0c9-4091-b242-ceb331004dfd"
    response = await make_get_request(f"genres/{genre_id}")
    assert response.status == HTTPStatus.NOT_FOUND
