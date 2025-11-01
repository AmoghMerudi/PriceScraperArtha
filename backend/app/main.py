from fastapi import FastAPI
from app.api import products

app = FastAPI(title = "Price Scraper API")
app.include_router(products.router)