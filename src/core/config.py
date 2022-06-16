
import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'Read-only API для онлайн-кинотеатра')

# Настройки Redis
#REDIS_HOST = os.getenv('REDIS_HOST', 'api-redis') 
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')#для локальной отладки
#REDIS_PORT = int(os.getenv('REDIS_PORT', 7379))
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))#для локальной отладки

# Настройки Elasticsearch
#ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'es')
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')#для локальной отладки
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))