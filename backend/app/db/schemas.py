from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    url: str
    site: str
    title: Optional[str] = None
    image_url: Optional[str] = None

class ProductOut(ProductBase):
    id: str = Field(..., description = "MongoDB document id")
    created_at: datetime

    class Config:
        orm_mode = True