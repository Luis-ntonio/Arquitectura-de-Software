# database.py
import uuid
import bcrypt  # type: ignore
import datetime
from typing import Dict, Any, List
from models import Case, Document, Attachment

# Simulated tables (dictionaries)
users_db: Dict[str, Dict] = {}                # Users DB
cases_db: Dict[str, Dict] = {}                # Cases DB
documents_db: Dict[str, Dict] = {}            # Documents DB
attachments_db: Dict[str, Dict] = {}          # Attachments DB

# Helper functions
def generate_id() -> str:
    return str(uuid.uuid4())

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

# CRUD Functions

# Users CRUD
async def create_user(username: str, password: str, role: str, email: str) -> Dict[str, Any]:
    user_id = generate_id()
    hashed_password = hash_password(password)
    user = {
        "id": user_id,
        "username": username,
        "password": hashed_password,
        "role": role,
        "created_at": datetime.datetime.now(),
        "email": email
    }
    users_db[user_id] = user
    return user

async def get_user_by_username(username: str) -> Dict[str, Any]:
    for user_id, user_data in users_db.items():
        if user_data["username"] == username:
            return {"user_id": user_id, **user_data}
    return None

# Cases CRUD
async def create_case(attorney_id: str, client_id: str, status: str, additional_info: str) -> Dict[str, Any]:
    case_id = generate_id()
    case = {
        "id": case_id,
        "attorney_id": attorney_id,
        "client_id": client_id,
        "status": status,
        "additional_info": additional_info
    }
    cases_db[case_id] = case
    return case

async def get_case_by_id(case_id: str) -> Dict[str, Any]:
    return cases_db.get(case_id)

# Documents CRUD
async def create_document(case_id: str, file_path: str) -> Dict[str, Any]:
    document_id = generate_id()
    document = {
        "id": document_id,
        "case_id": case_id,
        "file_path": file_path,
        "uploaded_at": datetime.datetime.now()
    }
    documents_db[document_id] = document
    return document

async def get_documents_by_case_id(case_id: str) -> List[Dict[str, Any]]:
    return [doc for doc in documents_db.values() if doc["case_id"] == case_id]

# Attachments CRUD
async def create_attachment(document_id: str, file_path: str) -> Dict[str, Any]:
    attachment_id = generate_id()
    attachment = {
        "id": attachment_id,
        "document_id": document_id,
        "file_path": file_path,
        "uploaded_at": datetime.datetime.now()
    }
    attachments_db[attachment_id] = attachment
    return attachment

async def get_attachments_by_document_id(document_id: str) -> List[Dict[str, Any]]:
    return [att for att in attachments_db.values() if att["document_id"] == document_id]

# Initialize Sample Data
async def init_sample_data():
    """Initialize sample data for development and testing"""
    # Create sample users
    owner = await create_user(
        username="parking_owner",
        password="owner123",
        role="owner",
        email="owner@example.com"
    )
    client = await create_user(
        username="parking_client",
        password="client123",
        role="client",
        email="client@example.com"
    )

    # Create sample cases
    case = await create_case(
        attorney_id=owner["id"],
        client_id=client["id"],
        status="open",
        additional_info="Sample case for testing."
    )

    # Create sample documents
    document = await create_document(
        case_id=case["id"],
        file_path="/uploads/sample_document.pdf"
    )

    # Create sample attachments
    await create_attachment(
        document_id=document["id"],
        file_path="/uploads/sample_attachment.pdf"
    )
