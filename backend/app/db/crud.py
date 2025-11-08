from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models import Product

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_url(db: Session, url: str):
    return db.query(Product).filter(Product.url == url).first()

def add_or_update_product(db: Session, url: str, name: str, price_cents: int, currency: str, site: str):
    product = db.query(Product).filter(Product.url == url).first()
    if product:
        product.price_cents = price_cents
        product.currency = currency
        product.last_checked = datetime.utcnow()
    else:
        product = Product(
            url=url, name=name, price_cents=price_cents, currency=currency, site=site
        )
        db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False