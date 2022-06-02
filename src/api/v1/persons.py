from http import HTTPStatus
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from services.persons import PersonService, get_person_service
from services.films import FilmService, get_film_service
from api.v1.schemas import Films, Person
from core.utils import page_check

router = APIRouter()

# Внедряем PersonService с помощью Depends(get_person_service)
@router.get('/{person_id}', 
            response_model=Person,
            summary="Персона",
            description="Информация о персоне",
            response_description="ID персоны,полное имя,роль,фильмы",
            )
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:

        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    person_api = Person(uuid=person.id, full_name=person.full_name
                        , role=person.role)

    if person.film_ids is not None:
         person_api.film_ids = [film_id for film_id in person.film_ids]

    return person_api

def persons_val_check(page_number, page_size):
    page = page_check(page_number=page_number, page_size=page_size)
    return page

async def format_films(results) -> list[Films]:
    films = []
    if results.get("hits") is None:
        return films
    [films.append(
        Films(uuid=result.get("_id"),
             title=result.get("_source").get("title"),
             imdb_rating=result.get("_source").get("imdb_rating")
             )
    ) for result in results.get("hits").get("hits")]
    return films

async def format_persons(results) -> list[Person]:
    persons = []
    if results.get("hits") is None:
        return persons
    [persons.append(
        Person(uuid=result.get("_id"),
             full_name=result.get("_source").get("full_name"),
             role=result.get("_source").get("role"),
             film_ids=result.get("_source").get("film_ids")
             )
    ) for result in results.get("hits").get("hits")]
    return persons


@router.get("/search/",
            response_model=list[Person],
            summary="Поиск персоны",
            description="Полнотекстовый поиск по персонам",
            response_description="Полное имя персоны",
            tags=['Полнотекстовый поиск']
            )
async def search_persons(
        query: Optional[str] = None,
        sort: Optional[str] = None,
        page_number: Optional[int] = Query(None, alias="page[number]"),
        page_size: Optional[int] = Query(None, alias="page[size]"),
        person_service: PersonService = Depends(get_person_service)
) -> Optional[list[Person]]:
    page = persons_val_check(page_number, page_size)
    results = await person_service.get_persons(search_query=query, page=page, sort=sort)
    persons = await format_persons(results)
    return persons


@router.get("/{person_id}/films", response_model=list[Films],
            summary="Кинопроизведения по персоне",
            description="Список всех кинопроизведений, в которых участвовала персона",
            response_description="ID кинопроизведения,название,рейтинг",
            )
async def films_by_person_search(
    person_id: str,
    sort: Optional[str] = None,
    filter_person: Optional[list] = Query(None, alias="filter[person]"),
    page_number: Optional[int] = Query(None, alias="page[number]"),
    page_size: Optional[int] = Query(None, alias="page[size]"),
    film_service: FilmService = Depends(get_film_service)
) -> Optional[list[Films]]:

    page = persons_val_check(page_number, page_size)
    results = await film_service.get_films(search_query=None, person_id=person_id, sort=sort, filter=filter_person, page=page)
    films = await format_films(results)
    
    return films