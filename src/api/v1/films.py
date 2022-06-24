from http import HTTPStatus
from typing import List, Optional

from api.v1.schemas import Film, FilmPerson, Films, Person
from fastapi import APIRouter, Depends, HTTPException, Query
from services.films import FilmService, get_film_service
from services.paginator import page_check

router = APIRouter()

# Внедряем FilmService с помощью Depends(get_film_service)
@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Кинопроизведение",
    description="Просмотр информации об одном кинопроизведении",
    response_description="Название,рейтинг фильма,описание,жанры,актеры,сценаристы,режиссеры",
)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(item_id=film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum
        # Такой код будет более поддерживаемым
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    # Перекладываем данные из models.Film в Film
    # Обратите внимание, что у модели бизнес-логики есть поле description
    # Которое отсутствует в модели ответа API.
    # Если бы использовалась общая модель для бизнес-логики и формирования ответов API
    # вы бы предоставляли клиентам данные, которые им не нужны
    # и, возможно, данные, которые опасно возвращать
    film_api = Film(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
    )
    if film.genre is not None:
        # заменить на ID жанра когда будет доработан ETL
        # film_api.genre = [Genre(name=gen) for gen in film.genre]
        film_api.genre = film.genre
    if film.actors is not None:
        film_api.actors = [
            FilmPerson(uuid=act.id, full_name=act.name) for act in film.actors
        ]
    if film.writers is not None:
        film_api.writers = [
            FilmPerson(uuid=wrt.id, full_name=wrt.name) for wrt in film.writers
        ]
    if film.directors is not None:
        film_api.directors = [
            FilmPerson(uuid=dir.id, full_name=dir.name) for dir in film.directors
        ]
    return film_api


def films_val_check(filter_genre, sort, page_number, page_size):
    if filter_genre is not None:
        filter = {"genre": filter_genre}
    else:
        filter = None
    if sort is not None:
        if sort.startswith("-"):
            sort_out = sort[1:] + ":desc"
        else:
            sort_out = sort
    else:
        sort_out = None
    page = page_check(page_number=page_number, page_size=page_size)
    return filter, sort_out, page


async def format_films(results) -> List[Films]:
    films = []
    if results.get("hits") is None:
        return films
    [
        films.append(
            Films(
                uuid=result.get("_id"),
                title=result.get("_source").get("title"),
                imdb_rating=result.get("_source").get("imdb_rating"),
            )
        )
        for result in results.get("hits").get("hits")
    ]
    return films


@router.get(
    "/",
    response_model=List[Films],
    summary="Список кинопроизведений",
    description="Спис кинопроизведений с сортировкой и фильтром по жанрам",
    response_description="ID, название, рейтинг",
)
async def films(
    sort: Optional[str] = Query(None, regex="-imdb_rating|imdb_rating"),
    filter_genre: Optional[List] = Query(None, alias="filter[genre]"),
    page_number: Optional[int] = Query(None, alias="page[number]"),
    page_size: Optional[int] = Query(None, alias="page[size]"),
    film_service: FilmService = Depends(get_film_service),
) -> Optional[List[Films]]:
    filter, sort_out, page = films_val_check(filter_genre, sort, page_number, page_size)
    results = await film_service._get_all_items(
        search_query=None, person_id=None, sort=sort_out, filter=filter, page=page
    )
    films = await format_films(results)
    return films


@router.get(
    "/search/",
    response_model=List[Films],
    summary="Поиск кинопроизведений",
    description="Полнотекстовый поиск по кинопроизведениям",
    response_description="ID, название, рейтинг фильма",
    tags=["Полнотекстовый поиск"],
)
async def search_films(
    query: Optional[str] = None,
    sort: Optional[str] = None,
    filter_genre: Optional[List] = Query(None, alias="filter[genre]"),
    page_number: Optional[int] = Query(None, alias="page[number]"),
    page_size: Optional[int] = Query(None, alias="page[size]"),
    film_service: FilmService = Depends(get_film_service),
) -> Optional[List[Films]]:
    filter, sort, page = films_val_check(filter_genre, sort, page_number, page_size)
    results = await film_service._get_all_items(
        search_query=query, person_id=None, sort=sort, filter=filter, page=page
    )
    films = await format_films(results)
    return films
