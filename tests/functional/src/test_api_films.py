import asyncio
from http import HTTPStatus
import aiofiles
import json
import pytest

#from testdata.schemas.film_schema import ListFilm, DetailResponseFilm, FilmPagination
from ..settings import Settings
#from ..testdata import data_films
#from core.utils import make_cache_key

pytestmark = pytest.mark.asyncio

@pytest.fixture(scope="function")
async def expected_json_response(request):
    """
    Loads expected response from json file with same filename as function name
    """
    file = Settings.expected_response_dir.joinpath(f"{request.node.name}.json")
    async with aiofiles.open(file) as f:
        content = await f.read()
        response = json.loads(content)
    return response


@pytest.mark.asyncio
async def test_film_by_id(make_get_request, expected_json_response):
    film_id = "c4c5e3de-c0c9-4091-b242-ceb331004dfd"
    response = await make_get_request(f"films/{film_id}")
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response

@pytest.mark.asyncio
async def test_films(make_get_request, expected_json_response):
    response = await make_get_request("films/")
    assert response.status == 200
    assert len(response.body) == 10
    assert response.body == expected_json_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("page_size", "page_number"),
    ( (1, 1), (1, 2), (50, 1)) )
async def test_film_paging(make_get_request, page_size, page_number):
    response = await make_get_request("films/",
        {"page[number]": page_number, "page[size]": page_size} )

    assert response.status == 200
    assert len(response.body) == page_size


@pytest.mark.asyncio
async def test_film_search(make_get_request, expected_json_response):
    response = await make_get_request("films/search/",{"query": "Captian"})
    assert response.status == 200
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_film_search_error(make_get_request):
    response = await make_get_request("films/search/",{"query": "abcxyz"})
    assert response.status == 200
    assert len(response.body) == 0


@pytest.mark.asyncio
async def test_film_filter_genre(make_get_request, expected_json_response):
    response = await make_get_request("films/",
    {"filter[genre]": "237fd1e4-c98e-454e-aa13-8a13fb7547b5"}
    )
    assert response.status == 200
    assert response.body == expected_json_response