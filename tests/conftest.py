import pytest
import requests
from pymongo import MongoClient

# Configuration
API_URL = "http://localhost:8000"
MONGO_URI = "mongodb://localhost:27017"

@pytest.fixture(scope="session")
def mongo_db():
    """Connect directly to MongoDB to verify data consistency[cite: 49]."""
    client = MongoClient(MONGO_URI)
    db = client["oms_db"]
    yield db
    client.close()

@pytest.fixture
def new_order_payload():
    """Generates a random order for testing[cite: 45]."""
    return {
        "user_id": "user_test_01",
        "items": [
            {"product_id": "p100", "name": "Test Product", "price": 50, "quantity": 2}
        ],
        "total_price": 100,
        "status": "Pending"
    }

@pytest.fixture
def created_order(new_order_payload):
    """Helper that creates an order and cleans it up after the test."""
    response = requests.post(f"{API_URL}/orders", json=new_order_payload)
    order_id = response.json().get("_id")
    
    yield order_id  # Pass ID to the test
    
    # Teardown: Delete order after test 
    requests.delete(f"{API_URL}/orders/{order_id}")