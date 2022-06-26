from typing import Optional

from fastapi import Query


class PaginatedParams:
    def __init__(
        self,
        page_number: Optional[int] = Query(None, alias="page[number]"),
        page_size: Optional[int] = Query(None, alias="page[size]"),
    ):
        self.page_number = 1 if page_number is None else page_number
        self.page_size = 10 if page_size is None else page_size
