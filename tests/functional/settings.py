import os

from dotenv import load_dotenv

load_dotenv()

class Settings():
    es_host: str = os.getenv("ELASTIC_HOST_URL", 'localhost')
    es_port: int = os.getenv("ELASTIC_PORT", 9200)
    elastic_url: str = f"http://{es_host}:{es_port}"

    redis_host: str = os.getenv("REDIS_HOST_URL", 'localhost')
    redis_port: str = os.getenv("REDIS_TEST_PORT", 6379)
    redis_url: str = f"{redis_host}:{redis_port}"

    api_host: str = os.getenv("API_HOST", 'localhost')
    api_port: int = os.getenv("API_PORT", 8800)
    service_url: str = f"http://{api_host}:{api_port}"

    person_test_index: str = "persons_test"
    genre_test_index: str = "genres_test"
    movies_test_index: str = "movies_test"