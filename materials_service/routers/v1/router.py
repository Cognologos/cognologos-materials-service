from fastapi import APIRouter

from . import ping


router = APIRouter(prefix="/v1")


for i in [
    ping.router,
]:
    router.include_router(i)
