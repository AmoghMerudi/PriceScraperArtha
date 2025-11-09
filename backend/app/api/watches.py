from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.db.mongo import get_mongo_db

router =  APIRouter(prefix = "/api/watches", tags = ["Watches"])

db = get_mongo_db()

def serialize_watch(watch):
    watch["_id"] = str(watch["_id"])
    return watch

@router.post("/")
async def add_watch(product_id: str, desired_cents: int):
    watch = {
        "product_id": product_id,
        "desired_cents": desired_cents,
        "active": True,
        "created_at": None,
    }
    result = await db["watches"].insert_one(watch)
    watch["_id"] = str(result.inserted_id)
    return watch

@router.get("/")
async def list_wawtches():
    watches = []
    async for w in db["watches"].find():
        watches.append(serialize_watch(w))
    return watches

@router.delete("/{watch_id}")
async def delete_watch(watch_id: str):
    result = await db["watches"].delete_one({"_id": ObjectId(watch_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Watch not found")
    return {"message": "Watch deleted successfully"}