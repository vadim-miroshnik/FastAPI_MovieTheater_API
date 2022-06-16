from dotenv import load_dotenv
from pydantic import BaseSettings, Field
from pathlib import Path

load_dotenv()


class Settings(BaseSettings):
    es_host: str = Field("http://127.0.0.1", env="ELASTIC_HOST")
    es_port: str = Field("9200", env="ELASTIC_PORT")
    elastic_url: str = f"http://{es_host}:{es_port}"

    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: str = Field("7379", env="REDIS_PORT")
    redis_url: str = f"http://{redis_host}:{redis_port}"

    api_host: str = Field("http://127.0.0.1", env="API_HOST")
    api_port: str = Field("8000", env="API_PORT")
    service_url: str = f"http://{api_host}:{api_port}"
    
    person_cache_key: str = "person_test"
    genre_cache_key: str = "genre_test"
    movies_cache_key: str = "movies_test"

    responses_dir: Path = Field(
        "tests/functional/testdata/responses")