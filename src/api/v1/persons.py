from http import HTTPStatus
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query

from services.persons import PersonService, get_person_service
from services.films import FilmService, get_film_service
from api.v1.schemas import Films, Person
from services.paginator import page_check

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

def persons_val_check(filter_person, sort, page_number, page_size):
    if filter_person is not None:
        filter = {"person": filter_person}
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
    [films.append(
        Films(uuid=result.get("_id"),
             title=result.get("_source").get("title"),
             imdb_rating=result.get("_source").get("imdb_rating")
             )
    ) for result in results.get("hits").get("hits")]
    return films

async def format_persons(results) -> List[Person]:
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
            response_model=List[Person],
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
) -> Optional[List[Person]]:
    page = persons_val_check(page_number, page_size)
    results = await person_service._get_all_items(search_query=query,person_id=None,filter=None,page=page, sort=sort)
    persons = await format_persons(results)
    return persons


@router.get("/{person_id}/films", response_model=List[Films],
            summary="Кинопроизведения по персоне",
            description="Список всех кинопроизведений, в которых участвовала персона",
            response_description="ID кинопроизведения,название,рейтинг",
            )
async def films_by_person_search(
    person_id: str,
    sort: Optional[str] = None,
    filter_person: Optional[List] = Query(None, alias="filter[person]"),
    page_number: Optional[int] = Query(None, alias="page[number]"),
    page_size: Optional[int] = Query(None, alias="page[size]"),
    film_service: FilmService = Depends(get_film_service)
) -> Optional[List[Films]]:

    
    filter_person = 'person'
    filter, sort, page  = persons_val_check(filter_person, sort, page_number, page_size)
    results = await film_service._get_all_items(search_query=None,
                                                person_id=person_id,
                                                sort=sort,
                                                filter=filter,
                                                page=page)
    films = await format_films(results)
    
    return films