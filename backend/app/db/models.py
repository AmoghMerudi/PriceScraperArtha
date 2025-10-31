from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    site = Column(String, nullable=False)
    title = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)   
    product_id = Column(Integer, ForeignKey("products.id"))
    amount_cents = Column(Integer)
    currency = Column(String)
    seen_at = Column(DateTime(timezone=True), server_default=func.now())


class Watch(Base):
    __tablename__ = "watches"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    desired_cents = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())