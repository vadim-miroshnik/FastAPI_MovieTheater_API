from .schema_template import TEMPLATE_INDEX_BODY

FILM_WORK_TEST_INDEX_BODY: dict = {
    **TEMPLATE_INDEX_BODY,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {"raw": {"type": "keyword"}},
            },
            "description": {"type": "text", "analyzer": "ru_en"},
            "imdb_rating": {"type": "float"},
            "genre": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "directors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
        },
    },
}
