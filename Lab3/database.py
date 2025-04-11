import uuid
import datetime
from typing import Dict, Any, List, Optional
from models import *

# Simulated tables (dictionaries)
attorney_db: Dict[str, Attorney] = {}
client_db: Dict[str, Client] = {}
cases_db: Dict[str, Cases] = {}
attachments_db: Dict[str, Attachment] = {}


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


def generate_id() -> str:
    return str(uuid.uuid4())


# --- Attorney CRUD Operations ---

async def create_attorney(name: str, email: str, phone: str, type: str) -> Attorney:
    attorney_id = generate_id()
    attorney = Attorney(id=attorney_id, name=name, email=email, phone=phone, type=type)
    attorney_db[attorney_id] = attorney
    return attorney


async def get_attorney(attorney_id: str) -> Optional[Attorney]:
    return attorney_db.get(attorney_id)


async def get_all_attorneys() -> List[Attorney]:
    return list(attorney_db.values())


async def update_attorney(attorney_id: str, name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, type: Optional[str] = None) -> Optional[Attorney]:
    if attorney_id not in attorney_db:
        raise DatabaseError(f"Attorney with id {attorney_id} not found")
    attorney = attorney_db[attorney_id]
    if name is not None:
        attorney.name = name
    if email is not None:
        attorney.email = email
    if phone is not None:
        attorney.phone = phone
    if type is not None:
        attorney.type = type
    return attorney


async def delete_attorney(attorney_id: str) -> bool:
    if attorney_id not in attorney_db:
        raise DatabaseError(f"Attorney with id {attorney_id} not found")
    del attorney_db[attorney_id]
    return True


# --- Client CRUD Operations ---

async def create_client(name: str, email: str, phone: str, address: str) -> Client:
    client_id = generate_id()
    client = Client(id=client_id, name=name, email=email, phone=phone, address=address)
    client_db[client_id] = client
    return client


async def get_client(client_id: str) -> Optional[Client]:
    return client_db.get(client_id)


async def get_all_clients() -> List[Client]:
    return list(client_db.values())


async def update_client(client_id: str, name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, address: Optional[str] = None) -> Optional[Client]:
    if client_id not in client_db:
        raise DatabaseError(f"Client with id {client_id} not found")
    client = client_db[client_id]
    if name is not None:
        client.name = name
    if email is not None:
        client.email = email
    if phone is not None:
        client.phone = phone
    if address is not None:
        client.address = address
    return client


async def delete_client(client_id: str) -> bool:
    if client_id not in client_db:
        raise DatabaseError(f"Client with id {client_id} not found")
    del client_db[client_id]
    return True


# --- Cases CRUD Operations ---

async def create_case(name: str, status: str, description: str, attorney_id: Optional[str], client_id: str, attachment_id: Optional[str]) -> Cases:
    case_id = generate_id()
    case = Cases(id=case_id, name=name, status=status, description=description, attorney_id=attorney_id, client_id=client_id, attachment_id=attachment_id)
    cases_db[case_id] = case
    return case


async def get_case(case_id: str) -> Optional[Cases]:
    return cases_db.get(case_id)


async def get_all_cases() -> List[Cases]:
    return list(cases_db.values())


async def update_case(case_id: str, name: Optional[str] = None, status: Optional[str] = None, description: Optional[str] = None, attorney_id: Optional[str] = None, client_id: Optional[str] = None, attachment_id: Optional[str] = None) -> Optional[Cases]:
    if case_id not in cases_db:
        raise DatabaseError(f"Case with id {case_id} not found")
    case = cases_db[case_id]
    if name is not None:
        case.name = name
    if status is not None:
        case.status = status
    if description is not None:
        case.description = description
    if attorney_id is not None:
        case.attorney_id = attorney_id
    if client_id is not None:
        case.client_id = client_id
    if attachment_id is not None:
        case.attachment_id = attachment_id
    return case


async def delete_case(case_id: str) -> bool:
    if case_id not in cases_db:
        raise DatabaseError(f"Case with id {case_id} not found")
    del cases_db[case_id]
    return True


# --- Attachment CRUD Operations ---

async def create_attachment(name: str, type: str, size: int, url: str, case_id: str) -> Attachment:
    attachment_id = generate_id()
    attachment = Attachment(id=attachment_id, name=name, type=type, size=size, url=url, case_id=case_id)
    attachments_db[attachment_id] = attachment
    return attachment


async def get_attachment(attachment_id: str) -> Optional[Attachment]:
    return attachments_db.get(attachment_id)


async def get_all_attachments() -> List[Attachment]:
    return list(attachments_db.values())


async def update_attachment(attachment_id: str, name: Optional[str] = None, type: Optional[str] = None, size: Optional[int] = None, url: Optional[str] = None, case_id: Optional[str] = None) -> Optional[Attachment]:
    if attachment_id not in attachments_db:
        raise DatabaseError(f"Attachment with id {attachment_id} not found")
    attachment = attachments_db[attachment_id]
    if name is not None:
        attachment.name = name
    if type is not None:
        attachment.type = type
    if size is not None:
        attachment.size = size
    if url is not None:
        attachment.url = url
    if case_id is not None:
        attachment.case_id = case_id
    return attachment


async def delete_attachment(attachment_id: str) -> bool:
    if attachment_id not in attachments_db:
        raise DatabaseError(f"Attachment with id {attachment_id} not found")
    del attachments_db[attachment_id]
    return True


def init_sample_data():
    # Clear existing data
    attorney_db.clear()
    client_db.clear()
    cases_db.clear()
    attachments_db.clear()

    # Create sample users
    attorney_id = generate_id()
    client_id = generate_id()

    attorney_db[attorney_id] = Attorney(id=attorney_id, name="Juan", email="sarasebastian2@gmail.com", phone="936404731", type="penalista")

    client_db[client_id] = Client(id=client_id, name="Luis", email="luis@gmail.com", phone="999222333", address="Av. Lima 123")

    cases_db["1"] = Cases(id="1", name="Caso 1", status="Activo", description="Atentado contra la integridad fisica", attorney_id=attorney_id, client_id=client_id, attachment_id="1")
    cases_db["2"] = Cases(id="2", name="Caso 2", status="Terminado", description="Acoso", attorney_id=attorney_id, client_id=client_id, attachment_id="2")
    cases_db["3"] = Cases(id="3", name="Caso 3", status="Pendiente", description="Soborno", attorney_id=attorney_id, client_id=client_id, attachment_id="3")
    cases_db["4"] = Cases(id="4", name="Caso 4", status="Activo", description="Asesinato", attorney_id=attorney_id, client_id=client_id, attachment_id="4")

    attachments_db["1"] = Attachment(id="1", name="Prueba 1", type="PDF", size=1024, url="http://example.com/attachment1", case_id="1")
    attachments_db["2"] = Attachment(id="2", name="Prueba 2", type="Imagen", size=2048, url="http://example.com/attachment2", case_id="2")
    attachments_db["3"] = Attachment(id="3", name="Prueba 3", type="Video", size=5120, url="http://example.com/attachment3", case_id="3")
    attachments_db["4"] = Attachment(id="4", name="Prueba 4", type="Audio", size=2560, url="http://example.com/attachment4", case_id="4")

    return {
        "attorney_db": attorney_db,
        "client_db": client_db,
        "cases_db": cases_db,
        "attachments_db": attachments_db
    }