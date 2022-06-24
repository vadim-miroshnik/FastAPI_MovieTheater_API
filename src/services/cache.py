import json
from typing import Optional

from core.utils import make_cache_key

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class BaseCache:
    async def _get_item_from_cache(
        self, etlmodel: Optional[str], item_id: str
    ) -> Optional[dict]:

        key = make_cache_key(endpoint=self.endpoint, item_id=item_id)
        data = await self.redis.get(key)
        if not data:
            return None

        item = etlmodel.parse_raw(data)
        return item

    async def _put_item_to_cache(self, item: Optional[str], item_id: Optional[str]):

        key = make_cache_key(endpoint=self.endpoint, item_id=item_id)
        value = item.json()
        await self.redis.set(key=key, value=value, expire=CACHE_EXPIRE_IN_SECONDS)

    async def _get_all_items_from_cache(
        self,
        search_query: Optional[str],
        sort: Optional[str],
        filter: Optional[dict],
        page: dict,
    ):

        key = make_cache_key(
            endpoint=self.endpoint,
            search_query=search_query,
            sort=sort,
            filter=filter,
            page=page,
        )

        data = await self.redis.get(key)
        if not data:
            return None
        items = json.loads(data)
        return items

    async def _put_all_items_to_cache(
        self,
        model_items: Optional[str],
        search_query: Optional[str],
        sort: Optional[str],
        filter: Optional[dict],
        page: dict,
    ):

        key = make_cache_key(
            endpoint=self.endpoint,
            search_query=search_query,
            sort=sort,
            filter=filter,
            page=page,
        )
        value = json.dumps(model_items)
        await self.redis.set(key=key, value=value, expire=CACHE_EXPIRE_IN_SECONDS)
