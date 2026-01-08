import pytest
from bson import ObjectId


@pytest.mark.smoke
@pytest.mark.api
def test_create_order(mongo_db, new_order_payload, api_client):
    response = api_client.post("/orders", data=new_order_payload)
    assert response.status_code == 201
    data = response.json()
    
    # Verify API Response
    assert data["user_id"] == new_order_payload.user_id
    assert data["total_price"] == new_order_payload.total_price
    
    # Verify MongoDB Consistency
    db_record = mongo_db.orders.find_one({"_id": ObjectId(data["_id"])})
    assert db_record is not None
    assert db_record["status"] == "Pending"

@pytest.mark.api
def test_get_order(created_order, api_client):
    response = api_client.get(f"/orders/{created_order}")
    assert response.status_code == 200
    assert response.json()["_id"] == created_order

@pytest.mark.api
@pytest.mark.parametrize("new_status", ["Processing", "Shipped", "Delivered"])
def test_update_order_status(created_order, mongo_db, new_status, api_client):
    payload = {"status": new_status}
    response = api_client.put(f"/orders/{created_order}", data=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == new_status
    
    # Verify DB update
    db_record = mongo_db.orders.find_one({"_id": ObjectId(created_order)})
    assert db_record["status"] == new_status

@pytest.mark.api
def test_delete_order(created_order, mongo_db, api_client):
    response = api_client.delete(f"/orders/{created_order}")
    assert response.status_code == 204
    
    # Verify it's gone from DB
    db_record = mongo_db.orders.find_one({"_id": ObjectId(created_order)})
    assert db_record is None

@pytest.mark.negative
@pytest.mark.api
def test_update_non_existent_order(api_client):
    fake_id = "65fd8a1b1234567890abcd99"
    response = api_client.put(f"/orders/{fake_id}", data={"status": "Shipped"})
    assert response.status_code == 404