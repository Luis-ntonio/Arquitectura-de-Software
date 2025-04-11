# models.py
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class ReservationStatus(str, Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

class CocheraStatus(str, Enum):
    available = "available"
    reserved = "reserved"
    occupied = "occupied"
    maintenance = "maintenance"

class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    refunded = "refunded"
    failed = "failed"

# MODELO XYZ
class Distrito(BaseModel):
    id: str
    name: str

class Cochera(BaseModel):
    id: str
    location: str
    price: float
    status: CocheraStatus
    size: str

class Autos(BaseModel):
    id : str
    modelo: str
    marca: str
    color: str
    placa: str
    cochera_id: str

class Reserva(BaseModel):
    id: str
    cochera_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    status: ReservationStatus = ReservationStatus.active
    payment_status: PaymentStatus = PaymentStatus.pending

class Ticket(BaseModel):
    id: str
    reserva_id: str
    cochera_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    status: ReservationStatus = ReservationStatus.active

class Disponibilidad(BaseModel):
    cochera_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: CocheraStatus = CocheraStatus.available

class Tarifas(BaseModel):
    cochera_id: str
    tarifa_hora: float
    tarifa_dia: float
    tarifa_semana: float
    tarifa_mes: float





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
