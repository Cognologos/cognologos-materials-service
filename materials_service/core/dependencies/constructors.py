from typing import AsyncGenerator, Generator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from redis.asyncio import ConnectionPool, Redis

from materials_service.core.config import AppConfig


def app_config() -> AppConfig:
    return AppConfig.from_env()


def mongodb_client(mongodb_url: str) -> Generator[AsyncIOMotorClient, None, None]:
    client = AsyncIOMotorClient(mongodb_url)
    try:
        yield client
    finally:
        client.close()


async def get_mongodb_database(
    client: AsyncIOMotorClient, database_name: str = "user"
) -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    db = client[database_name]
    yield db


async def redis_pool(redis_url: str) -> AsyncGenerator[ConnectionPool, None]:
    pool = ConnectionPool.from_url(redis_url)
    yield pool
    await pool.aclose()


async def redis_conn(pool: ConnectionPool) -> AsyncGenerator[Redis, None]:
    conn = Redis(connection_pool=pool)
    try:
        yield conn
    finally:
        await conn.aclose()
