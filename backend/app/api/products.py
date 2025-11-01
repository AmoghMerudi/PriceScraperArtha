from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models

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