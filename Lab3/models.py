# models.py
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class Case(BaseModel):
    id: str
    attorney_id: str
    client_id: str
    status: str
    additional_info: Optional[str] = None

class Document(BaseModel):
    id: str
    case_id: str
    file_path: str
    uploaded_at: datetime

class Attachment(BaseModel):
    id: str
    document_id: str
    file_path: str
    uploaded_at: datetime

# Enum for user roles
class UserRole(str, Enum):
    owner = "owner"
    client = "client"

# Authentication Models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: UserRole
    email: str

class UserResponse(BaseModel):
    user_id: str
    username: str
    role: UserRole
    email: str
    created_at: str