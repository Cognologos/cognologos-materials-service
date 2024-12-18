from fastapi import APIRouter


router = APIRouter(prefix="/v1")

for i in []:
    router.include_router(i)
