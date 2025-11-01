from fastapi import APIRouter
from app.api import products, health

router = APIRouter(prefix = "/api/health", tags = ["Health"])

@router.get("/")
def health_check():
    return {"status": "ok"}