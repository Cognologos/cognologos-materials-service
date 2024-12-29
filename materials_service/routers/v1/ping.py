from fastapi import APIRouter

from materials_service.core.dependencies.fastapi import DatabaseDependency
from materials_service.lib.db import ping as ping_db
from materials_service.lib.schemas.ping import PingSchema


router = APIRouter(prefix="/ping")


@router.post("/")
async def post_ping(db: DatabaseDependency) -> PingSchema:
    return await ping_db.make_ping(db)


@router.get("/")
async def get_ping(db: DatabaseDependency) -> PingSchema:
    return await ping_db.get_ping(db)
