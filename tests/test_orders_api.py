import pytest
import requests
from bson import ObjectId

API_URL = "http://localhost:8000"

# 1. Test Order Creation [cite: 45]
def test_create_order(mongo_db, new_order_payload):
    response = requests.post(f"{API_URL}/orders", json=new_order_payload)
    assert response.status_code == 201
    data = response.json()
    
    # Verify API Response
    assert data["user_id"] == new_order_payload["user_id"]
    
    # Verify MongoDB Consistency [cite: 49]
    db_record = mongo_db.orders.find_one({"_id": ObjectId(data["_id"])})
    assert db_record is not None
    assert db_record["status"] == "Pending"

# 2. Test Fetch Order [cite: 46]
def test_get_order(created_order):
    response = requests.get(f"{API_URL}/orders/{created_order}")
    assert response.status_code == 200
    assert response.json()["_id"] == created_order

# 3. Test Update Status (Parameterized) [cite: 54]
@pytest.mark.parametrize("new_status", ["Processing", "Shipped", "Delivered"])
def test_update_order_status(created_order, mongo_db, new_status):
    payload = {"status": new_status}
    response = requests.put(f"{API_URL}/orders/{created_order}", json=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == new_status
    
    # Verify DB update
    db_record = mongo_db.orders.find_one({"_id": ObjectId(created_order)})
    assert db_record["status"] == new_status

# 4. Test Delete Order [cite: 48]
def test_delete_order(created_order, mongo_db):
    response = requests.delete(f"{API_URL}/orders/{created_order}")
    assert response.status_code == 204 # Or 200 depending on API spec
    
    # Verify it's gone from DB
    db_record = mongo_db.orders.find_one({"_id": ObjectId(created_order)})
    assert db_record is None

# 5. Error Handling [cite: 50]
def test_update_non_existent_order():
    fake_id = "65fd8a1b1234567890abcd99"
    response = requests.put(f"{API_URL}/orders/{fake_id}", json={"status": "Shipped"})
    assert response.status_code == 404