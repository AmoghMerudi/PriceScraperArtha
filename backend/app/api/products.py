from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.db.mongo import get_mongo_db
from app.scraping.registry import get_scraper

db = get_mongo_db()

router = APIRouter(prefix="/api/products", tags=["Products"])

# Helper to convert Mongo _id to string for JSON responses
def serialize_product(product):
    product["_id"] = str(product["_id"])
    return product


@router.get("/")
async def list_products():
    products = []
    async for product in db["products"].find():
        products.append(serialize_product(product))
    return products


@router.post("/")
async def add_product(url: str, site: str):
    existing = await db["products"].find_one({"url": url})
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")

    product = {"url": url, "site": site}
    result = await db["products"].insert_one(product)
    product["_id"] = str(result.inserted_id)
    return product

@router.post("/scrape")
async def scrape_product(url: str, site: str):
    product = await db["products"].find_one({"url": url})
    if not product:
        product_doc = {"url": url, "site": site}
        result = await db["products"].insert_one(product_doc)
        product_doc["_id"] = str(result.inserted_id)
        product = product_doc

    scraper = get_scraper(site)
    quote = await scraper.fetch(url)

    if not quote.price_cents:
        return {"message": "No price found", "url": url}

    price_doc = {
        "product_id": str(product["_id"]),
        "amount_cents": quote.price_cents,
        "currency": quote.currency,
    }
    await db["prices"].insert_one(price_doc)

    return {"message": "Price Logged", "price": quote.price_cents / 100, "currency": quote.currency}


@router.get("/{product_id}")
async def get_product(product_id: str):
    try:
        product = await db["products"].find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return serialize_product(product)


@router.delete("/{product_id}")
async def remove_product(product_id: str):
    try:
        result = await db["products"].delete_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}