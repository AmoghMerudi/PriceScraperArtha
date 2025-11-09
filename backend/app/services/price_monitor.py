from bson import ObjectId
from app.db.mongo import get_mongo_db
from app.scraping.registry import get_scraper

db = get_mongo_db()

async def check_watches():
    print("🔎 Checking all active watches...")
    async for watch in db["watches"].find({"active": True}):
        product = await db["products"].find_one({"_id": ObjectId(watch["product_id"])})
        if not product:
            print(f"⚠️ Product not found for watch {watch['_id']}")
            continue

        scraper = get_scraper(product["site"])
        quote = await scraper.fetch(product["url"])

        if not quote or not quote.price_cents:
            print(f"❌ No price found for {product['url']}")
            continue

        if quote.price_cents <= watch["desired_cents"]:
            await db["alerts"].insert_one({
                "watch_id": str(watch["_id"]),
                "product_id": str(product["_id"]),
                "price_cents": quote.price_cents,
                "currency": quote.currency,
            })
            await db["watches"].update_one(
                {"_id": watch["_id"]},
                {"$set": {"active": False}}
            )
            print(f"💸 Price alert created for {product['url']}")
        else:
            print(f"⏳ {product['url']} still above target.")