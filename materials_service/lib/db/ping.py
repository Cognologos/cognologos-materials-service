from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from materials_service.lib.schemas.ping import PingSchema


async def make_ping(db: AsyncIOMotorDatabase) -> PingSchema:
    col = _get_collection(db)
    id = (await col.insert_one({"ping": True})).inserted_id
    return PingSchema.model_validate({"_id": id})


async def get_ping(db: AsyncIOMotorDatabase) -> PingSchema:
    col = _get_collection(db)
    res = await col.find_one({})
    if res is None:
        raise ValueError
    return PingSchema.model_validate(res)


def _get_collection(db: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return db.get_collection("ping")
