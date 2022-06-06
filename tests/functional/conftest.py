from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .settings import Settings


@pytest.fixture(scope="module")
def resource_setup():
    settings = Settings()
    return {"service_url": settings.service_url,
            "elastic_url": settings.elastic_url,
            "redis_url": settings.redis_url}


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture()
async def es_client(resource_setup):
    es_client = AsyncElasticsearch(hosts=resource_setup["elastic_url"])
    yield es_client
    await es_client.close()


@pytest.fixture()
async def redis_client(resource_setup):
    redis = await aioredis.create_redis_pool(resource_setup["redis_url"])
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture()
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
async def make_get_request(session, resource_setup):
    async def inner(endpoint: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = resource_setup["service_url"] + '/api/v1' + endpoint
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
