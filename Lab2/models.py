# models.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum for user roles
class UserRole(str, Enum):
    owner = "owner"
    client = "client"

# Enum for reservation status
class ReservationStatus(str, Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

# Enum for cochera status
class CocheraStatus(str, Enum):
    available = "available"
    reserved = "reserved"
    occupied = "occupied"
    maintenance = "maintenance"

# Enum for payment status
class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    refunded = "refunded"
    failed = "failed"

# Authentication Models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: UserRole
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: str
    username: str
    role: UserRole
    email: EmailStr
    created_at: str

# Cochera Models
class CocheraCreate(BaseModel):
    location: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)
    amenities: Optional[List[str]] = []
    size: str = "Standard"

class CocheraUpdate(BaseModel):
    location: Optional[str]
    price: Optional[float] = Field(None, gt=0)
    status: Optional[CocheraStatus]
    amenities: Optional[List[str]]
    size: Optional[str]

class CocheraResponse(BaseModel):
    cochera_id: str
    owner_id: str
    location: str
    price: float
    status: CocheraStatus
    created_at: str
    amenities: List[str]
    size: str
    rating_avg: float
    reviews_count: int

# Reservation Models
class ReservaCreate(BaseModel):
    cochera_id: str
    start_time: str
    end_time: str

class ReservaUpdate(BaseModel):
    status: Optional[ReservationStatus]
    payment_status: Optional[PaymentStatus]

class ReservaResponse(BaseModel):
    reserva_id: str
    user_id: str
    cochera_id: str
    start_time: str
    end_time: str
    status: ReservationStatus
    created_at: str
    price_total: float
    payment_status: PaymentStatus

# Review Models
class ReviewCreate(BaseModel):
    cochera_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=3, max_length=500)

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=3, max_length=500)

class ReviewResponse(BaseModel):
    review_id: str
    user_id: str
    cochera_id: str
    rating: int
    comment: str
    created_at: str

# Payment Models
class PaymentCreate(BaseModel):
    reserva_id: str
    amount: float
    payment_method: str = "credit_card"

class PaymentResponse(BaseModel):
    payment_id: str
    reserva_id: str
    amount: float
    status: PaymentStatus
    created_at: str