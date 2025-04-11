# database.py
import uuid
import datetime
from typing import Dict, Any
from models import *

# Simulated tables (dictionaries)
attorney_db: Dict[str, Attorney] = {}
client_db: Dict[str, Client] = {}
cases_db: Dict[str, Cases] = {}
attachments_db: Dict[str, Attachment] = {}

def generate_id() -> str:
    return str(uuid.uuid4())

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
