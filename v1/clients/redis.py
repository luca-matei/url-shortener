import redis
import redis.asyncio as async_redis

from v1.config import settings


class RedisConnectionPoolManager:
    _pools = {}

    @classmethod
    def get_pool(cls, db, is_async, decode_responses):
        key = (db, is_async)
        if key not in cls._pools:
            if is_async:
                cls._pools[key] = async_redis.ConnectionPool(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    username=settings.redis_user,
                    password=settings.redis_password,
                    db=db,
                    decode_responses=decode_responses,
                )
            else:
                cls._pools[key] = redis.ConnectionPool(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    username=settings.redis_user,
                    password=settings.redis_password,
                    db=db,
                    decode_responses=decode_responses,
                )
        return cls._pools[key]


class RedisSession:
    def __init__(self, db=0, decode="utf-8"):
        self.db = db
        self.decode_responses = decode == "utf-8"
        self.is_async = False
        self.connection = None
        self.pool = RedisConnectionPoolManager.get_pool(
            db, self.is_async, self.decode_responses
        )

    def __enter__(self):
        if self.is_async:
            raise RuntimeError("Use 'async with' for async mode")
        self.connection = redis.Redis(connection_pool=self.pool)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    async def __aenter__(self):
        self.is_async = True
        self.pool = RedisConnectionPoolManager.get_pool(
            self.db, self.is_async, self.decode_responses
        )
        self.connection = async_redis.Redis(connection_pool=self.pool)
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()


if __name__ == "__main__":
    # Usage example for synchronous code
    with RedisSession(db=0, decode="utf-8") as cache:
        cache.set("key", "value")
        print(cache.get("key"))
