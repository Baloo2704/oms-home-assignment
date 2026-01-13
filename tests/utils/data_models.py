from pydantic import BaseModel, Field
from typing import List, Optional
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
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None