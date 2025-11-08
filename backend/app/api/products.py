from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models
from app.db.models import Product, Price
from app.scraping.registry import get_scraper 
from app.db import crud, database
from app.db.models import Base

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.post("/")
def add_product(url:str, site: str, db: Session = Depends(get_db)):
    existing =  db.query(models.Product).filter_by(url = url).first()
    if existing:
        raise HTTPException(status_code = 400, detail = "Product")
    product = models.Product(url = url, site = site)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.post("/scrape")
async def scrape_product(url: str, site: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.url == url).first()

    if not product:
        product = models.Product(url=url, site=site)
        db.add(product)
        db.commit()
        db.refresh(product)

    scraper = get_scraper(site)
    quote = await scraper.fetch(url)

    if not quote.price_cents:
        return {"message": "No price found", "url": url}

    new_price = models.Price(
        product_id=product.id,
        amount_cents=quote.price_cents,
        currency=quote.currency
    )
    db.add(new_price)
    db.commit()

    return {"message": "Price Logged", "price": quote.price_cents / 100, "currency": quote.currency}

Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(crud.Product).filter(crud.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}