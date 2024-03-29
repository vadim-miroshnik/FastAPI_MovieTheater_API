from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_film_by_id(make_get_request, expected_json_response):
    film_id = "c4c5e3de-c0c9-4091-b242-ceb331004dfd"
    response = await make_get_request(f"films/{film_id}")
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_film_by_wrong_id(make_get_request):
    film_id = "11111111-c0c9-4091-b242-ceb331004dfd"
    response = await make_get_request(f"films/{film_id}")
    assert response.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_films(make_get_request, expected_json_response):
    response = await make_get_request("films/", {"page[number]": 1, "page[size]": 10})
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 10
    assert response.body == expected_json_response


@pytest.mark.asyncio
@pytest.mark.parametrize(("page_size", "page_number"), ((1, 1), (1, 2), (50, 1)))
async def test_film_paging(make_get_request, page_size, page_number):
    response = await make_get_request(
        "films/", {"page[number]": page_number, "page[size]": page_size}
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body) == page_size


@pytest.mark.asyncio
async def test_film_search(make_get_request, expected_json_response):
    response = await make_get_request("films/search/", {"query": "Captain"})
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response


@pytest.mark.asyncio
async def test_film_search_error(make_get_request):
    response = await make_get_request("films/search/", {"query": "abcxyz"})
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 0


@pytest.mark.asyncio
async def test_film_filter_genre(make_get_request, expected_json_response):
    response = await make_get_request(
        "films/",
        {
            "filter[genre]": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
            "page[number]": 1,
            "page[size]": 10,
        },
    )
    assert response.status == HTTPStatus.OK
    assert response.body == expected_json_response
