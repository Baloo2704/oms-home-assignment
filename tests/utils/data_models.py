from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

class OrderPayload(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_price: float
    status: str = "Pending"
    created_at: datetime = datetime.now()