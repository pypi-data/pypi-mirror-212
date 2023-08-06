from typing import Optional, Any
from .abc import AbstractCache
from croydon.middleware import req_cache_ctx


class RequestLocalCache(AbstractCache):
    NAME = "RequestLocalCache"

    async def initialise(self) -> None:
        pass

    async def get(self, key: str) -> Optional[Any]:
        cache = req_cache_ctx.get()
        if cache is None:
            return None
        return cache.get(key)

    async def set(self, key: str, value: Any) -> None:
        cache = req_cache_ctx.get()
        if cache is None:
            return
        cache[key] = value
        req_cache_ctx.set(cache)

    async def has(self, key: str) -> bool:
        cache = req_cache_ctx.get()
        if cache is None:
            return False
        return key in cache

    async def delete(self, key: str) -> bool:
        had = await self.has(key)
        if had:
            cache = req_cache_ctx.get()
            del cache[key]
            req_cache_ctx.set(cache)
        return had
