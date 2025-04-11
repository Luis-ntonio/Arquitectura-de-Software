import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

try:
    from main import app
    from database import users_db, documents_db, cases_db, attachments_db, init_sample_data
except ImportError as e:
    print(f"Error importing FastAPI app or database: {e}")
    app = None

# --- Fixtures ---

@pytest.fixture(scope="module")
def client():
    """
    Pytest fixture to create a TestClient instance for the FastAPI app.
    """
    if app is None:
        pytest.fail("FastAPI app could not be imported.")
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function", autouse=True)
def reset_data_before_each_test():
    """
    Fixture to reset the in-memory data before each test function runs.
    """
    if app:
        init_sample_data()

# --- Test Data ---
OWNER_USER = {"username": "parking_owner", "password": "owner123"}
CLIENT_USER = {"username": "parking_client", "password": "client123"}
NEW_USER = {"username": "new_tester", "password": "testpassword", "role": "client", "email": "tester@example.com"}

# --- Helper Functions ---

def get_user_id(client: TestClient, user_credentials):
    """Helper to log in and get user ID."""
    response = client.post("/api/auth/login", json=user_credentials)
    if response.status_code == 200:
        return response.json().get("user_id")
    return None

# --- Test Functions ---

# == Authentication Tests (/api/auth) ==

def test_register_user_success(client: TestClient):
    """Test successful user registration."""
    response = client.post("/api/auth/register", json=NEW_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == NEW_USER["username"]
    assert "user_id" in data
    assert data["user_id"] in users_db

def test_register_new_owner(client: TestClient):
    """Test the happy path of registering a new owner."""
    new_owner = {
        "username": "new_owner",
        "password": "ownerpassword",
        "role": "owner",
        "email": "new_owner@example.com"
    }
    response = client.post("/auth/register", json=new_owner)
    assert response.status_code == 200
    data = response.json()

    # Verify the new owner is registered
    assert data["username"] == new_owner["username"]
    assert data["role"] == "owner"
    assert data["email"] == new_owner["email"]
    assert data["user_id"] in users_db

def test_login_success(client: TestClient):
    """Test successful user login for owner and client."""
    response_owner = client.post("/api/auth/login", json=OWNER_USER)
    assert response_owner.status_code == 200
    assert response_owner.json()["username"] == OWNER_USER["username"]
    assert response_owner.json()["role"] == "owner"

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

# == Cases Tests (/cases) ==

def test_create_case(client: TestClient):
    """Test creating a new case."""
    new_case = {
        "id": "case_123",
        "attorney_id": "attorney_1",
        "client_id": "client_1",
        "status": "open",
        "additional_info": "Test case details."
    }
    response = client.post("/cases/", json=new_case)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == new_case["id"]
    assert cases_db[new_case["id"]]["status"] == "open"

def test_update_case_status(client: TestClient):
    """Test updating the status of a case."""
    case_id = next(iter(cases_db.keys()))
    response = client.patch(f"/status/{case_id}", json={"status": "in_progress"})
    assert response.status_code == 200
    assert cases_db[case_id]["status"] == "in_progress"

def test_invalid_case_status_transition(client: TestClient):
    """Test invalid status transition for a case."""
    case_id = next(iter(cases_db.keys()))
    response = client.patch(f"/status/{case_id}", json={"status": "open"})
    assert response.status_code == 400

# == Documents Tests (/documents) ==

def test_upload_document(client: TestClient):
    """Test uploading a document for a case."""
    case_id = next(iter(cases_db.keys()))
    file_content = b"Sample document content"
    file_name = "sample_document.pdf"

    response = client.post(
        f"/documents/upload/?case_id={case_id}",
        files={"file": (file_name, file_content, "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == case_id
    assert "file_path" in data
    assert data["file_path"].endswith(".pdf")

# == Attachments Tests (/attachments) ==

def test_upload_attachment_success(client: TestClient):
    """Test uploading an attachment for a document."""
    document_id = next(iter(documents_db.keys()))
    file_content = b"Sample attachment content"
    file_name = "sample_attachment.pdf"

    response = client.post(
        f"/attachments/upload/?document_id={document_id}",
        files={"file": (file_name, file_content, "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == document_id
    assert "file_path" in data
    assert data["file_path"].endswith(".pdf")

def test_upload_attachment_invalid_document(client: TestClient):
    """Test uploading an attachment for a non-existent document."""
    invalid_document_id = "non_existent_doc"
    file_content = b"Sample attachment content"
    file_name = "sample_attachment.pdf"

    response = client.post(
        f"/attachments/upload/?document_id={invalid_document_id}",
        files={"file": (file_name, file_content, "application/pdf")},
    )
    assert response.status_code == 404

def test_client_hires_owner_and_attaches_documents(client: TestClient):
    """Test the happy path of a client hiring an owner for a case and attaching documents."""
    # Step 1: Client logs in
    client_login_response = client.post("/auth/login", json=CLIENT_USER)
    assert client_login_response.status_code == 200
    client_data = client_login_response.json()
    client_id = client_data["user_id"]

    # Step 2: Owner logs in
    owner_login_response = client.post("/auth/login", json=OWNER_USER)
    assert owner_login_response.status_code == 200
    owner_data = owner_login_response.json()
    owner_id = owner_data["user_id"]

    # Step 3: Client creates a new case with the owner
    new_case = {
        "id": "case_456",
        "attorney_id": owner_id,
        "client_id": client_id,
        "status": "open",
        "additional_info": "Client hiring owner for a legal case."
    }
    case_response = client.post("/cases/", json=new_case)
    assert case_response.status_code == 200
    case_data = case_response.json()
    case_id = case_data["id"]

    # Step 4: Client uploads a document for the case
    file_content = b"Sample case document content"
    file_name = "case_document.pdf"
    document_response = client.post(
        f"/documents/upload/?case_id={case_id}",
        files={"file": (file_name, file_content, "application/pdf")},
    )
    assert document_response.status_code == 200
    document_data = document_response.json()
    document_id = document_data["id"]

    # Step 5: Client uploads an attachment for the document
    attachment_content = b"Sample attachment content"
    attachment_name = "case_attachment.pdf"
    attachment_response = client.post(
        f"/attachments/upload/?document_id={document_id}",
        files={"file": (attachment_name, attachment_content, "application/pdf")},
    )
    assert attachment_response.status_code == 200
    attachment_data = attachment_response.json()

    # Verify the attachment is linked to the document
    assert attachment_data["document_id"] == document_id
    assert "file_path" in attachment_data
    assert attachment_data["file_path"].endswith(".pdf")

