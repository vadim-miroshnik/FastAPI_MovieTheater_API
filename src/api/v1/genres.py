from http import HTTPStatus
from typing import List, Optional

from api.v1.schemas import Genre
from core.pagination import PaginatedParams
# from models.genre import Genre as ESGenre
from fastapi import APIRouter, Depends, HTTPException, Query
from services.genres import GenreService, get_genre_service
from services.paginator import items_val_check

router = APIRouter()

# Внедряем GenreService с помощью Depends(get_genre_service)


@router.get(
    "/{item_id}",
    response_model=Genre,
    summary="Жанр",
    description="Жанр кинопроизведения",
    response_description="ID жанра, название",
)
async def genre_details(
    item_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(item_id=item_id)
    if not genre:

        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")

    genre_api = Genre(uuid=genre.id, name=genre.name)
    return genre_api


async def format_genres(results) -> List[Genre]:
    genres = []
    if results.get("hits") is None:
        return genres
    [
        genres.append(
            Genre(uuid=result.get("_id"), name=result.get("_source").get("name"))
        )
        for result in results.get("hits").get("hits")
    ]
    return genres


@router.get(
    "/",
    response_model=List[Genre],
    summary="Жанры",
    description="Список жанров кинопроизведений",
    response_description="ID жанра, название",
)
async def genres(
    sort: Optional[str] = None,
    pagination: PaginatedParams = Depends(PaginatedParams),
    genre_service: GenreService = Depends(get_genre_service),
) -> Optional[List[Genre]]:
    sort, page = items_val_check(sort, pagination.page_number, pagination.page_size)
    results = await genre_service._get_all_items(
        search_query=None, person_id=None, filter=None, sort=sort, page=page
    )

    genres = await format_genres(results)
    return genres
