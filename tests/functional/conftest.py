import asyncio
import json
from dataclasses import dataclass

import aiofiles
import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from . import es_index, testdata
from .settings import Settings
from .utils.es_inserter import es_index_loader

settings = Settings()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def person_index(es_client):
    index: str = Settings.person_test_index
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.PERSON_TEST_INDEX_BODY,
        row_data=testdata.data_person,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture
async def genre_index(es_client):
    index: str = Settings.genre_test_index
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.GENRE_TEST_INDEX_BODY,
        row_data=testdata.data_genre,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture
async def movies_index(es_client):
    index: str = Settings.movies_test_index
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.FILM_WORK_TEST_INDEX_BODY,
        row_data=testdata.data_films,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture()
async def es_client():
    es_client = AsyncElasticsearch(hosts=Settings.elastic_url)
    yield es_client
    await es_client.close()


@pytest.fixture()
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
async def make_get_request(session):
    async def inner(endpoint: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = Settings.service_url + "/api/v1/" + endpoint
        async with session.get(url, params=params) as response:
            response = HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
            return response

    return inner


@pytest.fixture(scope="function")
async def expected_json_response(request):
    """
    Loads expected response from json file with same filename as function name
    """
    file = settings.responses_dir.joinpath(f"{request.node.name}.json")
    async with aiofiles.open(file) as f:
        content = await f.read()
        response = json.loads(content)
    return response
