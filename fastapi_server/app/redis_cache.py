import json
import hashlib
import logging
from typing import Dict, Any, Optional
import redis

from app.config import settings

logger = logging.getLogger(__name__)

class RedisCacheManager:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.memory_fallback: Dict[str, Dict[str, Any]] = {}
        self._connect()

    def _connect(self):
        try:
            client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD or None,
                decode_responses=True,
                socket_timeout=0.5,
                socket_connect_timeout=0.5
            )
            if client.ping():
                self.redis_client = client
                logger.info(f"Connected to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        except Exception as e:
            logger.warning(f"Redis connection unavailable ({e}). Using in-memory fallback cache.")
            self.redis_client = None

    def _get_key(self, url: str) -> str:
        url_clean = url.strip().lower()
        md5_hash = hashlib.md5(url_clean.encode("utf-8")).hexdigest()
        return f"adtech:crawl:{md5_hash}"

    def get(self, url: str) -> Optional[Dict[str, Any]]:
        key = self._get_key(url)
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(key)
                if cached_data:
                    logger.info(f"Cache HIT in Redis for: {url}")
                    return json.loads(cached_data)
            except Exception as e:
                logger.warning(f"Error reading Redis key {key}: {e}")

        if key in self.memory_fallback:
            logger.info(f"Cache HIT in Memory Fallback for: {url}")
            return self.memory_fallback[key]

        logger.info(f"Cache MISS for: {url}")
        return None

    def set(self, url: str, data: Dict[str, Any], ttl: int = settings.CACHE_TTL_SECONDS):
        key = self._get_key(url)
        json_str = json.dumps(data, ensure_ascii=False)

        if self.redis_client:
            try:
                self.redis_client.setex(key, ttl, json_str)
                logger.info(f"Cached crawl data in Redis for {url} (TTL={ttl}s)")
                return
            except Exception as e:
                logger.warning(f"Error writing Redis key {key}: {e}")

        self.memory_fallback[key] = data

    def flush(self) -> bool:
        self.memory_fallback.clear()
        if self.redis_client:
            try:
                keys = self.redis_client.keys("adtech:crawl:*")
                if keys:
                    self.redis_client.delete(*keys)
                logger.info("Cleared all adtech crawl keys from Redis.")
                return True
            except Exception as e:
                logger.error(f"Error clearing Redis cache: {e}")
                return False
        return True

    def get_stats(self) -> Dict[str, Any]:
        if not self.redis_client:
            return {
                "redis_available": False,
                "connected_clients": 0,
                "used_memory_human": "0B",
                "total_keys": len(self.memory_fallback),
                "adtech_cache_keys": len(self.memory_fallback)
            }

        try:
            info = self.redis_client.info()
            adtech_keys = len(self.redis_client.keys("adtech:crawl:*"))
            return {
                "redis_available": True,
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "total_keys": self.redis_client.dbsize(),
                "adtech_cache_keys": adtech_keys
            }
        except Exception as e:
            return {
                "redis_available": False,
                "error": str(e),
                "total_keys": len(self.memory_fallback),
                "adtech_cache_keys": len(self.memory_fallback)
            }

cache_manager = RedisCacheManager()
