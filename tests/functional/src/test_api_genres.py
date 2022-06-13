import asyncio
from http import HTTPStatus

import pytest

from testdata.schemas.genre_schema import FilmGenre, GenrePagination
from ..settings import Settings
from ..testdata import data_genre
from core.utils import make_cache_key

pytestmark = pytest.mark.asyncio

async def test_genres_list(make_get_request, redis_client):
    await asyncio.sleep(3)
    # Выполнение запроса
    response = await make_get_request(endpoint="genres/")
    response_body = response.body
    response_genres = response_body.get("genres")
    # Проверка результата Elastic
    assert response.status == HTTPStatus.OK
    assert GenrePagination(**response_body)
    assert response_body.get("total") == len(data_genre)
    for genre in data_genre:
        for response_genre in response_genres:
            if genre.get("id") == response_genre.get("uuid"):
                assert genre.get("id") == response_genre.get("uuid")
                assert genre.get("name") == response_genre.get("name")
    # Проверка результата Redis
    page: int = response_body.get("page")
    page_size: int = response_body.get("page_size")
    total: int = response_body.get("total")
    key: str = make_cache_key(
        endpoint=Settings.person_cache_key, params=f"{total}{page}{page_size}"
    )
    assert await redis_client.get(key=key) is not None
    await redis_client.flushall()
    assert await redis_client.get(key=key) is None


async def test_genre_by_id(make_get_request, redis_client):
    for test_genre in data_genre:
        genre_id: str = test_genre.get("id")
        # Выполнение запроса
        response = await make_get_request(endpoint=f"genres/{genre_id}")
        response_body = response.body
        # Проверка результата Elastic
        assert response.status == HTTPStatus.OK
        assert FilmGenre(**response_body)
        assert test_genre.get("id") == response_body.get("uuid")
        assert test_genre.get("name") == response_body.get("name")
        # Проверка результата Redis
        assert await redis_client.get(key=genre_id) is not None
        await redis_client.flushall()
        assert await redis_client.get(key=genre_id) is None