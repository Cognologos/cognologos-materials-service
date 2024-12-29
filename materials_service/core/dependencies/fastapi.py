from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from redis.asyncio import ConnectionPool, Redis as AbstractRedis

from materials_service.core.config import AppConfig

from . import constructors as app_depends


def db_client_stub() -> AsyncIOMotorClient:
    raise NotImplementedError


def app_config_stub() -> AppConfig:
    raise NotImplementedError


async def db_session(
    request: Request,
    client: Annotated[AsyncIOMotorClient, Depends(db_client_stub)],
) -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    generator = app_depends.get_mongodb_database(client, "user")
    session = await anext(generator)
    request.state.db = session

    yield session

    try:
        await anext(generator)
    except StopAsyncIteration:
        pass
    else:
        raise RuntimeError("Database session not closed (db dependency generator is not closed).")


def redis_conn_pool_stub() -> ConnectionPool:
    raise NotImplementedError


async def redis_conn(
    request: Request, conn_pool: Annotated[ConnectionPool, Depends(redis_conn_pool_stub)]
) -> AsyncGenerator[AbstractRedis, None]:
    generator = app_depends.redis_conn(conn_pool)
    redis = await anext(generator)
    request.state.redis = redis

    yield redis

    try:
        await anext(generator)
    except StopAsyncIteration:
        pass
    else:
        raise RuntimeError("Redis session not closed (redis dependency generator is not closed).")


RedisDependency = Annotated[AbstractRedis, Depends(redis_conn)]
DatabaseDependency = Annotated[AsyncIOMotorDatabase, Depends(db_session)]
