from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from materials_service.core.config import AppConfig
from materials_service.core.dependencies import constructors as app_depends, fastapi as stubs
from materials_service.core.exceptions.abc import AbstractException
from materials_service.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    config = AppConfig.from_env()
    async with asynccontextmanager(app_depends.redis_pool)(config.redis.url) as redis_pool:
        with contextmanager(app_depends.mongodb_client)(config.database.url) as client:
            app.dependency_overrides[stubs.app_config_stub] = lambda: config
            app.dependency_overrides[stubs.db_client_stub] = lambda: client
            app.dependency_overrides[stubs.redis_conn_pool_stub] = lambda: redis_pool

            yield


app = FastAPI(
    lifespan=lifespan,
)


@app.exception_handler(AbstractException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": True, "message": exc.detail})


app.include_router(router)
