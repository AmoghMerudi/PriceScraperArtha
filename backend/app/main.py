from fastapi import FastAPI
from app.api import products, health, watches
from app.services.scheduler import start_scheduler  

app = FastAPI(title="Price Scraper API")

app.include_router(products.router)
app.include_router(health.router)
app.include_router(watches.router)

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    print("✅ App started with background scheduler.")