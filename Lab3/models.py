from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class Attorney(BaseModel):
    id: Optional[str] = None  # Add id, make it optional for creation
    name: str
    email: str
    phone: str
    type: str

class Client(BaseModel):
    id: Optional[str] = None  # Add id, make it optional for creation
    name: str
    email: str
    phone: str
    address: str

class Cases(BaseModel):
    id: Optional[str] = None  # Add id, make it optional for creation
    name: str
    status: str
    description: str
    attorney_id: Optional[str] = None
    client_id: str
    attachment_id : Optional[str] = None

class Attachment(BaseModel):
    id: Optional[str] = None  # Add id, make it optional for creation
    name: str
    type: str
    size: int
    url: str
    case_id: str