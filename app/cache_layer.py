import hashlib
import json
import logging
from collections.abc import Callable

from config import settings
from redis import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

REDIS_URL = settings.REDIS_URL
SEARCH_TTL = settings.CACHE_SEARCH_TTL
PRODUCT_TTL = settings.CACHE_PRODUCT_TTL

def make_key(operation: str, params: dict) -> str:
    serialized = json.dumps(params, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return f"dixie:mock:v1:{operation}:{digest}"

def get_or_load(operation: str, params: dict, ttl: int, loader: Callable[[], dict]) -> dict:
    key = make_key(operation, params)

    with Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1, socket_timeout=1) as client:
        try:
            cached = client.get(key)
        except RedisError as exc:
            logger.warning("cache_unavailable operation=%s error=%s", operation, type(exc).__name__)
            return loader()

        if cached is not None:
            try:
                result = json.loads(cached)
                if not isinstance(result, dict):
                    raise ValueError("Cache response must be an object.")
            except ValueError:
                logger.warning("cache_invalid key=%s", key)
            else:
                logger.info("cache_hit key=%s", key)
                return result

        logger.info("cache_miss key=%s", key)
        result = loader()

        if result.get("products"):
            try:
                client.set(key, json.dumps(result, ensure_ascii=False), ex=ttl)
            except RedisError as exc:
                logger.warning("cache_write_failed key=%s error=%s", key, type(exc).__name__)

        return result