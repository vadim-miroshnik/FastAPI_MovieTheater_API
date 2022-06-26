from typing import Optional

import aioredis
from aioredis import Redis
from core import config

redis: Optional[Redis] = None

# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT), encoding="utf-8"
    )
    return redis
