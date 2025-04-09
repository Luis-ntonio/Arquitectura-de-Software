# models.py
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

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
    end_time: datetime
    status: CocheraStatus = CocheraStatus.available

class Tarifas(BaseModel):
    cochera_id: str
    tarifa_hora: float
    tarifa_dia: float
    tarifa_semana: float
    tarifa_mes: float