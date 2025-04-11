# database.py
import uuid
import datetime
from typing import Dict, Any, List
from models import *

# Simulated tables (dictionaries)
attorney_db: Dict[str, Attorney] = {}
client_db: Dict[str, Client] = {}
cases_db: Dict[str, Cases] = {}
attachments_db: Dict[str, Attachment] = {}

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

async def update_attorney(attorney_id: str, name: str = None, email: str = None, phone: str = None, type: str = None) -> Optional[Attorney]:
    if attorney_id in attorney_db:
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
    return None

async def delete_attorney(attorney_id: str) -> bool:
    if attorney_id in attorney_db:
        del attorney_db[attorney_id]
        return True
    return False

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

async def update_client(client_id: str, name: str = None, email: str = None, phone: str = None, address: str = None) -> Optional[Client]:
    if client_id in client_db:
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
    return None

async def delete_client(client_id: str) -> bool:
    if client_id in client_db:
        del client_db[client_id]
        return True
    return False

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

async def update_case(case_id: str, name: str = None, status: str = None, description: str = None, attorney_id: Optional[str] = None, client_id: str = None, attachment_id: Optional[str] = None) -> Optional[Cases]:
    if case_id in cases_db:
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
    return None

async def delete_case(case_id: str) -> bool:
    if case_id in cases_db:
        del cases_db[case_id]
        return True
    return False

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

async def update_attachment(attachment_id: str, name: str = None, type: str = None, size: int = None, url: str = None, case_id: str = None) -> Optional[Attachment]:
    if attachment_id in attachments_db:
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
    return None

async def delete_attachment(attachment_id: str) -> bool:
    if attachment_id in attachments_db:
        del attachments_db[attachment_id]
        return True
    return False





def init_sample_data():
    # Clear existing data
    attorney_db.clear()
    client_db.clear()
    cases_db.clear()
    attachments_db.clear()
    
    # Create sample users
    attorney_id = generate_id()
    client_id = generate_id()
    
    attorney_db[attorney_id] = create_attorney("Juan", "sarasebastian2@gmail.com", "936404731", "penalista")
    
    client_db[client_id] = create_client("Luis", "luis@gmail.com", "999222333", "Av. Lima 123")
    
    cases_db["1"] = create_case("Caso 1", "Activo", "Atentado contra la integridad fisica", attorney_id, client_id, "1")
    cases_db["2"] = create_case("Caso 2", "Terminado", "Acoso", attorney_id, client_id, "2")
    cases_db["3"] = create_case("Caso 3", "Pendiente", "Soborno", attorney_id, client_id, "3")
    cases_db["4"] = create_case("Caso 4", "Activo", "Asesinato", attorney_id, client_id, "4")
    
    attachments_db["1"] = create_attachment("Prueba 1", "PDF", 1024, "http://example.com/attachment1", "1")
    attachments_db["2"] = create_attachment("Prueba 2", "Imagen", 2048, "http://example.com/attachment2", "2")
    attachments_db["3"] = create_attachment("Prueba 3", "Video", 5120, "http://example.com/attachment3", "3")
    attachments_db["4"] = create_attachment("Prueba 4", "Audio", 2560, "http://example.com/attachment4", "4")
    
    return {
        "attorney_db": attorney_db,
        "client_db": client_db,
        "cases_db": cases_db,
        "attachments_db": attachments_db
    }
