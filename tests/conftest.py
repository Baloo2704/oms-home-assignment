import pytest
import logging
from pymongo import MongoClient
from tests.utils.api_client import APIClient
from tests.utils.data_models import OrderPayload, OrderItem


# Configuration
API_URL = "http://localhost:8000"
MONGO_URI = "mongodb://localhost:27017"

# Logger Fixture
@pytest.fixture(scope="session")
def logger():
    """Returns a configured logger instance."""
    logger = logging.getLogger("oms_tests")
    return logger

@pytest.fixture(scope="function", autouse=True)
def log_test_lifecycle(logger, request):
    """Automatically logs the start and end of every test."""
    test_name = request.node.name
    
    # Log Start
    logger.info(f"\n{'='*20} TEST START: {test_name} {'='*20}")
    
    yield  # The test runs here
    
    # Log End
    logger.info(f"{'='*20} TEST END: {test_name} {'='*20}")

@pytest.fixture(scope="session")
def api_client(logger):
    """
    Returns an instance of APIClient that automatically logs
    all requests and responses.
    """
    return APIClient(base_url=API_URL, logger=logger)

@pytest.fixture(scope="session")
def mongo_db(logger): 
    """Connect directly to MongoDB to verify data consistency."""
    logger.info(f"Connecting to MongoDB at {MONGO_URI}...")
    try:
        client = MongoClient(MONGO_URI)
        db = client["oms_db"]
        # Ping the DB to ensure connection works
        client.admin.command('ping')
        logger.info("MongoDB connection successful.")
        yield db
        client.close()
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        pytest.fail("Database connection failed")

@pytest.fixture
def new_order_payload():
    """Generates a valid order object using Pydantic."""
    return OrderPayload(
        user_id="user_test_01",
        items=[
            OrderItem(product_id="p100", name="Test Product", price=50.0, quantity=2)
        ],
        total_price=100.0,
        status="Pending"
    )

@pytest.fixture
def created_order(api_client, new_order_payload, logger):
    """Helper that creates an order and cleans it up after the test."""
    logger.info("Setup: Creating order...")
    
    response = api_client.post("/orders", data=new_order_payload)
    assert response.status_code == 201
    
    order_id = response.json().get("_id")
    
    yield order_id  # Pass ID to the test
    
    logger.info(f"Teardown: Deleting order {order_id}...")
    api_client.delete(f"/orders/{order_id}")