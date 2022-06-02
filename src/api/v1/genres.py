from http import HTTPStatus
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from services.genres import GenreService, get_genre_service
from api.v1.schemas import Genre
from core.utils import page_check

router = APIRouter()

# Внедряем GenreService с помощью Depends(get_genre_service)
@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:

        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    
    genre_api = Genre(uuid=genre.id, name=genre.name)
    return genre_api


def genres_val_check(sort, page_number, page_size):
    if sort is not None:
        sort = sort + ":desc"
    page = page_check(page_number=page_number, page_size=page_size)
    return sort, page


async def format_genres(results) -> list[Genre]:
    genres = []
    if results.get("hits") is None:
        return genres
    [genres.append(
        Genre(uuid=result.get("_id"),
              name=result.get("_source").get("name")
             )
    ) for result in results.get("hits").get("hits")]
    return genres


@router.get("/")
async def genres(
        sort: Optional[str] = None,
        page_number: Optional[int] = Query(None, alias="page[number]"),
        page_size: Optional[int] = Query(None, alias="page[size]"),
        genre_service: GenreService = Depends(get_genre_service)
) -> Optional[list[Genre]]:
    sort, page = genres_val_check(sort, page_number, page_size)
    results = await genre_service.get_all_genres(search_query=None, sort=sort, page=page)
    genres = await format_genres(results)
    return genres