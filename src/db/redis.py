import json
from typing import Optional, Any
from aioredis import Redis
import aioredis
from core import config

redis: Optional[Redis] = None

# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), encoding='utf-8')
    return redis


async def get_redis_data(redis_client: Redis, key: dict) -> Any:
    data = await redis_client.get(key)
    if not data:
        return None
    return data


async def set_redis_data(redis_client: Redis, key: dict, value: json, expire: int) -> None:
    await redis_client.set(key, value, expire=expire)