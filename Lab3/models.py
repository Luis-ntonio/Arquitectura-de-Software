from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class Attorney(BaseModel):
    name: str
    email: str
    phone: str
    type: str

class Client(BaseModel):
    name: str
    email: str
    phone: str
    address: str

class Cases(BaseModel):
    name: str
    status: str
    description: str
    attorney_id: str
    client_id: str
    attachment_id : str

class Attachment(BaseModel):
    name: str
    type: str
    size: int
    url: str
    case_id: str
