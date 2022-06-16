from typing import Any, Dict, List, Union

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default=None):
    return orjson.dumps(v, default=default).decode()


class BaseWithJsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseListRootModel(BaseWithJsonModel):
    __root__: List

    def __iter__(self):
        return self.__root__.__iter__()

    def __getitem__(self, item):
        return self.__root__.__getitem__(item)


class MultiMatchQuerySchema(BaseWithJsonModel):
    query: str
    fields: List[str]
    fuzziness: str = "AUTO"


class MultiMatchSchema(BaseWithJsonModel):
    multi_match: MultiMatchQuerySchema


class MatchSchema(BaseWithJsonModel):
    match: Dict[str, Any]


class MustSchema(BaseWithJsonModel):
    must: List[BaseWithJsonModel]


class TermSchema(BaseWithJsonModel):
    term: Dict[str, Any]


class ShouldSchema(BaseWithJsonModel):
    should: List[BaseWithJsonModel]


class BoolSchema(BaseWithJsonModel):
    bool: Dict[str, List[BaseWithJsonModel]]


class OrderSchema(BaseWithJsonModel):
    order: str


class SortSchema(BaseWithJsonModel):
    sort: Dict[str, OrderSchema]


class QuerySchema(BaseWithJsonModel):
    query: BoolSchema


class NestedSchema(BaseWithJsonModel):
    path: str
    query: BoolSchema


class FilterSchema(BaseWithJsonModel):
    nested: NestedSchema


class RootQuerySchema(BaseWithJsonModel):
    __root__: Dict[str, Union[BoolSchema, SortSchema]]


class DocSchema(BaseWithJsonModel):
    source: Dict[str, Any] = Field(..., alias="_source")


class HitsSchema(BaseWithJsonModel):
    hits: List[DocSchema]


class ResponseSchema(BaseWithJsonModel):
    hits: HitsSchema
