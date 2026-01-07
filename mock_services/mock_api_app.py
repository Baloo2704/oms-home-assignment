# main.py
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

app = FastAPI()

# Connect to the MongoDB we just started
client = MongoClient("mongodb://localhost:27017")
db = client["oms_db"]
orders_collection = db["orders"]

# --- Pydantic Models (Matching Assignment Schema [cite: 27]) ---
class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_price: float

class OrderUpdate(BaseModel):
    status: str

# --- API Endpoints ---

@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    # Logic: Validate and Store [cite: 16, 17]
    order_dict = order.dict()
    order_dict["status"] = "Pending"
    order_dict["created_at"] = datetime.utcnow()
    
    new_order = orders_collection.insert_one(order_dict)
    
    # Return the Created Order with ID
    order_dict["_id"] = str(new_order.inserted_id)
    return order_dict

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    # Logic: Fetch by ID [cite: 46]
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    order = orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    order["_id"] = str(order["_id"]) # Convert ObjectId to string for JSON
    return order

@app.put("/orders/{order_id}")
def update_status(order_id: str, update: OrderUpdate):
    # Logic: Update Status (e.g., Pending -> Shipped) [cite: 47]
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": update.status}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return {"status": update.status, "message": "Updated successfully"}

@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: str):
    # Logic: Delete Order [cite: 48]
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    result = orders_collection.delete_one({"_id": ObjectId(order_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return