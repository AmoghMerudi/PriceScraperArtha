from fastapi import FastAPI
from app.api import products, health

app = FastAPI(title = "Price Scraper API")

app.include_router(products.router)
app.include_router(health.router)