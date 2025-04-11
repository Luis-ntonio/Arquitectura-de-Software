import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

# Assuming your main FastAPI app instance is in 'main.py'
# Adjust the import path if your file structure is different
try:
    from main import app
    # Import database directly to check state or reset if needed (optional)
    from database import users_db, cocheras_db, reservas_db, reviews_db, init_sample_data
except ImportError as e:
    print(f"Error importing FastAPI app or database: {e}")
    print("Please ensure 'main.py' and 'database.py' are accessible.")
    app = None # Avoid further errors if import fails


# --- Fixtures ---

@pytest.fixture(scope="module")
def client():
    """
    Pytest fixture to create a TestClient instance for the FastAPI app.
    Manages the app's lifespan, including startup (init_sample_data).
    """
    if app is None:
        pytest.fail("FastAPI app could not be imported.")
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function", autouse=True)
def reset_data_before_each_test():
    """
    Fixture to reset the in-memory data before each test function runs.
    Ensures tests are independent. Runs automatically for every test.
    """
    if app: # Only run if app was imported successfully
        # print("\nResetting sample data...") # Optional: uncomment for verbose output
        init_sample_data() # Re-initialize data

# --- Test Data ---
# Common user credentials for testing
OWNER_USER = {"username": "parking_owner", "password": "owner123"}
CLIENT_USER = {"username": "parking_client", "password": "client123"}
NEW_USER = {"username": "new_tester", "password": "testpassword", "role": "client", "email": "tester@example.com"}

# --- Helper Function to get User ID ---
def get_user_id(client: TestClient, user_credentials):
    """Helper to log in and get user ID."""
    response = client.post("/api/auth/login", json=user_credentials)
    if response.status_code == 200:
        return response.json().get("user_id")
    return None

# --- Test Functions ---

# == Core Authentication Tests (/api/auth) ==

def test_register_user_success(client: TestClient):
    """Test successful user registration."""
    response = client.post("/api/auth/register", json=NEW_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == NEW_USER["username"]
    assert "user_id" in data
    # Verify user is in the database
    assert data["user_id"] in users_db

def test_login_success(client: TestClient):
    """Test successful user login for owner and client."""
    # Test Owner Login
    response_owner = client.post("/api/auth/login", json=OWNER_USER)
    assert response_owner.status_code == 200
    assert response_owner.json()["username"] == OWNER_USER["username"]
    assert response_owner.json()["role"] == "owner"

    # Test Client Login
    response_client = client.post("/api/auth/login", json=CLIENT_USER)
    assert response_client.status_code == 200
    assert response_client.json()["username"] == CLIENT_USER["username"]
    assert response_client.json()["role"] == "client"

def test_login_wrong_password(client: TestClient):
    """Test login with incorrect password."""
    response = client.post("/api/auth/login", json={
        "username": OWNER_USER["username"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401


# == Core Cocheras Tests (/api/cocheras) ==

def test_list_cocheras_basic(client: TestClient):
    """Test listing all cocheras without filters."""
    response = client.get("/api/cocheras/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4 # Based on sample data
    assert "cochera_id" in data[0]

def test_get_cochera_success(client: TestClient):
    """Test retrieving a specific cochera by ID."""
    list_resp = client.get("/api/cocheras/")
    cochera_id = list_resp.json()[0]["cochera_id"] # Get first cochera ID
    response = client.get(f"/api/cocheras/{cochera_id}")
    assert response.status_code == 200
    assert response.json()["cochera_id"] == cochera_id

def test_get_cochera_not_found(client: TestClient):
    """Test retrieving a non-existent cochera."""
    response = client.get("/api/cocheras/non-existent-id")
    assert response.status_code == 404

def test_create_cochera_owner_success(client: TestClient):
    """Test creating a new cochera as an owner."""
    new_cochera_data = {"location": "San Borja", "price": 9.0}
    payload = {**new_cochera_data, **OWNER_USER} # Combine data and owner credentials
    response = client.post("/api/cocheras/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == new_cochera_data["location"]
    assert data["status"] == "available"
    assert data["cochera_id"] in cocheras_db # Verify creation

def test_update_cochera_owner_success(client: TestClient):
    """Test updating a cochera successfully by its owner."""
    # Get a cochera owned by OWNER_USER
    owner_id = get_user_id(client, OWNER_USER)
    owner_cocheras = [cid for cid, cdata in cocheras_db.items() if cdata.get("owner_id") == owner_id]
    assert owner_cocheras, "No cocheras found for the owner to update."
    cochera_id = owner_cocheras[0]

    update_payload = {
        "update_data": {"price": 8.5, "status": "maintenance"},
        **OWNER_USER # Add owner credentials
    }
    response = client.patch(f"/api/cocheras/{cochera_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 8.5
    assert data["status"] == "maintenance"
    assert cocheras_db[cochera_id]["status"] == "maintenance" # Verify change in DB

def test_delete_cochera_owner_success(client: TestClient):
    """Test deleting an available cochera successfully by its owner."""
    # Create a cochera specifically for deletion
    create_payload = {"location": "To Delete", "price": 1.0, **OWNER_USER}
    create_resp = client.post("/api/cocheras/", json=create_payload)
    assert create_resp.status_code == 200
    cochera_id_to_delete = create_resp.json()["cochera_id"]

    # Delete the cochera
    delete_payload = OWNER_USER
    response = client.request("DELETE", f"/api/cocheras/{cochera_id_to_delete}", json=delete_payload)
    assert response.status_code == 204
    assert cochera_id_to_delete not in cocheras_db # Verify deletion
    get_resp = client.get(f"/api/cocheras/{cochera_id_to_delete}") # Verify it's gone
    assert get_resp.status_code == 404

def test_delete_cochera_with_active_reservation_fails(client: TestClient):
    """Test deleting a cochera with an active reservation fails."""
    # Find the initially reserved cochera ID
    reserved_cochera = next((c for c_id, c in cocheras_db.items() if c["status"] == "reserved"), None)
    assert reserved_cochera is not None, "Sample data should have a reserved cochera."
    cochera_id_to_delete = next(c_id for c_id, c in cocheras_db.items() if c["status"] == "reserved")

    delete_payload = OWNER_USER
    response = client.request("DELETE", f"/api/cocheras/{cochera_id_to_delete}", json=delete_payload)
    assert response.status_code == 400 # Should fail due to active reservation
    assert "active reservations" in response.json()["detail"]


# == Core Reservas Tests (/api/reservas) ==

def test_list_reservations_client(client: TestClient):
    """Test listing reservations for the logged-in client."""
    client_id = get_user_id(client, CLIENT_USER)
    response = client.get("/api/reservas/", json={"username": CLIENT_USER["username"]})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1 # Client has initial reservation
    if data: # Check owner if list is not empty
       assert all(item.get("user_id") == client_id for item in data)

def test_get_reservation_client_success(client: TestClient):
    """Test getting a specific reservation as the client who made it."""
    # Find the client's reservation ID from the DB
    client_id = get_user_id(client, CLIENT_USER)
    reserva_id = next((rid for rid, r in reservas_db.items() if r.get("user_id") == client_id), None)
    assert reserva_id is not None, "Client should have an initial reservation."

    response = client.get(f"/api/reservas/{reserva_id}", json={"username": CLIENT_USER["username"]})
    assert response.status_code == 200
    assert response.json()["reserva_id"] == reserva_id

def test_create_reservation_client_success(client: TestClient):
    """Test creating a reservation successfully as a client."""
    # Find an available cochera ID
    available_cochera = next((cid for cid, c in cocheras_db.items() if c["status"] == "available"), None)
    assert available_cochera is not None, "No available cocheras in sample data."
    cochera_id = available_cochera

    start_time = (datetime.now() + timedelta(days=1)).isoformat()
    end_time = (datetime.now() + timedelta(days=1, hours=2)).isoformat()
    reservation_data = {
        "reserva": {"cochera_id": cochera_id, "start_time": start_time, "end_time": end_time},
        "username": CLIENT_USER["username"]
    }
    response = client.post("/api/reservas/", json=reservation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["cochera_id"] == cochera_id
    assert data["status"] == "active"
    assert data["reserva_id"] in reservas_db # Verify creation
    assert cocheras_db[cochera_id]["status"] == "reserved" # Verify cochera status update

def test_update_reservation_client_cancel_success(client: TestClient):
    """Test a client cancelling their own reservation."""
    # Find the client's active reservation ID
    client_id = get_user_id(client, CLIENT_USER)
    reserva_id = next((rid for rid, r in reservas_db.items() if r.get("user_id") == client_id and r.get("status") == "active"), None)
    assert reserva_id is not None, "Client should have an active reservation to cancel."
    cochera_id = reservas_db[reserva_id]["cochera_id"]

    update_payload = {
        "update_data": {"status": "cancelled"},
        "username": CLIENT_USER["username"]
    }
    response = client.patch(f"/api/reservas/{reserva_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"
    assert reservas_db[reserva_id]["status"] == "cancelled" # Verify in DB
    assert cocheras_db[cochera_id]["status"] == "available" # Verify cochera available


# == Core Reviews Tests (/api/reviews) ==

@pytest.fixture(scope="function")
def completed_reservation_for_review(client: TestClient):
    """Fixture to ensure a completed reservation exists for review testing."""
    # Find an available cochera
    available_cochera_id = next((cid for cid, c in cocheras_db.items() if c["status"] == "available"), None)
    if not available_cochera_id:
         pytest.skip("No available cocheras to create a reservation for review.")

    # Create reservation as client
    start_time = (datetime.now() + timedelta(minutes=1)).isoformat() # Short times for testing
    end_time = (datetime.now() + timedelta(minutes=5)).isoformat()
    create_payload = {
        "reserva": {"cochera_id": available_cochera_id, "start_time": start_time, "end_time": end_time},
        "username": CLIENT_USER["username"]
    }
    create_resp = client.post("/api/reservas/", json=create_payload)
    if create_resp.status_code != 200: pytest.fail("Failed to create reservation for review.")
    reserva_id = create_resp.json()["reserva_id"]

    # Mark as completed by owner
    complete_payload = {"update_data": {"status": "completed"}, "username": OWNER_USER["username"]}
    complete_resp = client.patch(f"/api/reservas/{reserva_id}", json=complete_payload)
    if complete_resp.status_code != 200: pytest.fail("Failed to complete reservation for review.")

    client_user_id = get_user_id(client, CLIENT_USER)
    return {"cochera_id": available_cochera_id, "user_id": client_user_id}

def test_list_reviews_basic(client: TestClient):
    """Test listing all reviews."""
    response = client.get("/api/reviews/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1 # Based on sample data
    if data:
        assert "review_id" in data[0]

def test_get_review_success(client: TestClient):
    """Test getting a specific review by ID."""
    # Get the ID of the initial review from sample data
    review_id = next(iter(reviews_db)) # Get first key (review_id)
    response = client.get(f"/api/reviews/{review_id}")
    assert response.status_code == 200
    assert response.json()["review_id"] == review_id

def test_create_review_client_success(client: TestClient, completed_reservation_for_review):
    """Test creating a review successfully after a completed reservation."""
    review_data = {
        "review": {
            "cochera_id": completed_reservation_for_review["cochera_id"],
            "rating": 5,
            "comment": "Great spot!"
        },
        "username": CLIENT_USER["username"]
    }
    response = client.post("/api/reviews/", json=review_data)
    assert response.status_code == 200
    data = response.json()
    assert data["cochera_id"] == completed_reservation_for_review["cochera_id"]
    assert data["user_id"] == completed_reservation_for_review["user_id"]
    assert data["rating"] == 5
    assert data["review_id"] in reviews_db # Verify creation

def test_create_review_fails_if_not_completed(client: TestClient):
    """Test creating review fails if user hasn't completed a reservation for it."""
    # Find a cochera the client hasn't used or completed reservation for
    cochera_id_never_used = None
    client_id = get_user_id(client, CLIENT_USER)
    client_completed_cocheras = {r['cochera_id'] for r in reservas_db.values() if r['user_id'] == client_id and r['status'] == 'completed'}
    
    for cid in cocheras_db:
        if cid not in client_completed_cocheras:
             # Check if there's an initial review for this cochera by the client already (from sample data)
             has_initial_review = any(rev['cochera_id'] == cid and rev['user_id'] == client_id for rev in reviews_db.values())
             if not has_initial_review:
                 cochera_id_never_used = cid
                 break # Found one

    assert cochera_id_never_used is not None, "Could not find a suitable cochera for this test."

    review_data = {
        "review": {"cochera_id": cochera_id_never_used, "rating": 4, "comment": "Trying to review."},
        "username": CLIENT_USER["username"]
    }
    response = client.post("/api/reviews/", json=review_data)
    assert response.status_code == 403 # Forbidden as reservation wasn't completed
    assert "only review parking spots you have used" in response.json()["detail"]


def test_update_review_author_success(client: TestClient):
    """Test updating a review successfully by its author."""
    # Find the initial review made by the client
    client_id = get_user_id(client, CLIENT_USER)
    review_id = next((rid for rid, r in reviews_db.items() if r.get("user_id") == client_id), None)
    assert review_id is not None, "Client should have an initial review to update."

    update_payload = {
        "update_data": {"rating": 5, "comment": "Updated comment!"},
        "username": CLIENT_USER["username"] # Author updating
    }
    response = client.patch(f"/api/reviews/{review_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["comment"] == "Updated comment!"
    assert reviews_db[review_id]["comment"] == "Updated comment!" # Verify in DB

