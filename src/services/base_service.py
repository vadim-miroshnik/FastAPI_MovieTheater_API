from operator import index
from typing import Optional

from elasticsearch import NotFoundError

from services.cache import BaseCache


class BaseService(BaseCache):
    async def get_by_id(self, item_id: str) -> Optional[dict]:

        item = await self._get_item_from_cache(etlmodel=self.etlmodel, item_id=item_id)

        if not item:
            item = await self._get_item_from_elastic(item_id=item_id)
            if not item:
                return None
            await self._put_item_to_cache(item=item, item_id=item_id)

        return item

    async def _get_all_items(
        self,
        search_query: str,
        page: int,
        person_id: str or None,
        filter: Optional[dict],
        sort: Optional[str],
    ):
        items = await self._get_all_items_from_cache(
            search_query=search_query, sort=sort, filter=filter, page=page
        )
        if not items:
            items = await self._get_all_items_from_elastic(
                search_query=search_query,
                person_id=person_id,
                sort=sort,
                filter=filter,
                page=page,
            )

            if not items:
                return None
            await self._put_all_items_to_cache(
                model_items=items,
                search_query=search_query,
                sort=sort,
                filter=filter,
                page=page,
            )

        return items

    async def _get_item_from_elastic(self, item_id: str) -> Optional[str]:

        try:
            doc = await self.elastic.get(index=self.index, id=item_id)
        except NotFoundError:
            return None
        return self.etlmodel(**doc["_source"])

    async def _get_all_items_from_elastic(
        self,
        search_query: Optional[str],
        person_id: str,
        sort: Optional[str],
        filter: Optional[dict],
        page: dict,
    ):
        body = {"query": {"bool": {"must": []}}}

        if filter is not None and self.index == "movies":

            if type(filter.get("genre")) is str:
                filter["genre"] = [
                    filter.get("genre"),
                ]

                for genre_id in filter.get("genre"):
                    body["query"]["bool"]["must"].append(
                        {
                            "nested": {
                                "path": "genre",
                                "query": {"match": {"genre.id": str(genre_id)}},
                            }
                        }
                    )

            elif type(filter.get("person")) is str:
                for field_name in ("directors", "actors", "writers"):
                    body["query"]["bool"]["must"].append(
                        {
                            "nested": {
                                "path": field_name,
                                "query": {
                                    "match": {f"{field_name}.id": str(person_id)}
                                },
                            }
                        }
                    )

        if search_query is not None:
            if self.index == "movies":
                body["query"]["bool"]["must"].append(
                    {"match": {"title": str(search_query)}}
                )
            elif self.index == "persons":
                body["query"]["bool"]["must"].append(
                    {"match": {"full_name": str(search_query)}}
                )
        if filter is None and search_query is None:
            body = None

        response = await self.elastic.search(
            index=self.index,
            from_=(page["number"] - 1) * page["size"],
            size=page["size"],
            request_timeout=5,
            sort=sort,
            body=body,
        )
        return response
