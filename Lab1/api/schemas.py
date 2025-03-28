from pydantic import BaseModel
from datetime import datetime

class SaleRequest(BaseModel):
    product_name: str
    quantity: int
    price: float

class SaleResponse(BaseModel):
    id: int
    created_at: datetime