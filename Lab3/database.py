# database.py
import uuid
import bcrypt # type: ignore
import datetime
from typing import Dict, Any
from models import (
    Distrito, Cochera, Autos, Reserva, Ticket, Disponibilidad, Tarifas,
    ReservationStatus, CocheraStatus, PaymentStatus
)
# from functions import cocheras 

# Simulated tables (dictionaries)
users_db: Dict[str, Dict] = {}                # Users DB
cases_db: Dict[str, Dict] = {}                # Cases DB
documents_db: Dict[str, Dict] = {}            # Documents DB
attachments_db: Dict[str, Dict] = {}          # Attachments DB

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

def get_user_by_username(username: str) -> Dict[str, Any]:
    for user_id, user_data in users_db.items():
        if user_data["username"] == username:
            return {"user_id": user_id, **user_data}
    return None

def init_sample_data():
    """Initialize sample data for development and testing"""
    # Clear existing data
    users_db.clear()
    cases_db.clear()
    documents_db.clear()
    attachments_db.clear()
    
    # Create sample users
    owner_id = generate_id()
    client_id = generate_id()
    
    users_db[owner_id] = {
        "id": owner_id,
        "username": "parking_owner",
        "password": hash_password("owner123"),
        "role": "owner",
        "created_at": datetime.datetime.now(),
        "email": "owner@example.com"
    }
    
    users_db[client_id] = {
        "id": client_id,
        "username": "parking_client",
        "password": hash_password("client123"),
        "role": "client",
        "created_at": datetime.datetime.now(),
        "email": "client@example.com"
    }

    # Create sample cases
    case_id = generate_id()
    cases_db[case_id] = {
        "id": case_id,
        "attorney_id": owner_id,
        "client_id": client_id,
        "status": "open",
        "additional_info": "Sample case for testing."
    }

    # Create sample documents
    document_id = generate_id()
    documents_db[document_id] = {
        "id": document_id,
        "case_id": case_id,
        "file_path": "/uploads/sample_document.pdf",
        "uploaded_at": datetime.datetime.now(),
    }

    # Create sample attachments
    attachment_id = generate_id()
    attachments_db[attachment_id] = {
        "id": attachment_id,
        "document_id": document_id,
        "file_path": "/uploads/sample_attachment.pdf",
        "uploaded_at": datetime.datetime.now(),
    }
