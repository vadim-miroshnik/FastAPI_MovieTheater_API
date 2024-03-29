import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class Settings:
    es_host: str = os.getenv("ELASTIC_HOST_URL", "localhost")
    es_port: int = os.getenv("ELASTIC_PORT", 9200)
    elastic_url: str = f"http://{es_host}:{es_port}"

    redis_host: str = os.getenv("REDIS_HOST_URL", "localhost")
    redis_port: str = os.getenv("REDIS_TEST_PORT", 6379)
    redis_url: str = f"{redis_host}:{redis_port}"

    api_host: str = os.getenv("API_HOST", "localhost")
    api_port: int = os.getenv("API_PORT", 8800)
    service_url: str = f"http://{api_host}:{api_port}"
    person_cache_key: str = "person_test"
    genre_cache_key: str = "genre_test"
    movies_cache_key: str = "movies_test"

    responses_dir: Path = Path("./functional/testdata/responses")
