# database.py
import uuid
import bcrypt
import datetime
from typing import Dict, Any
from Lab2.models import (
    Distrito, Cochera, Autos, Reserva, Ticket, Disponibilidad, Tarifas,
    ReservationStatus, CocheraStatus, PaymentStatus
)

# Simulated tables (dictionaries)
users_db: Dict[str, Dict] = {}                # Users DB
autos_db: Dict[str, Autos] = {}               # Autos DB
cocheras_db: Dict[str, Cochera] = {}          # Cocheras DB
reservas_db: Dict[str, Reserva] = {}          # Reservas DB
disponibilidad_db: Dict[str, Disponibilidad] = {}  # Disponibilidad DB
distrito_db: Dict[str, Distrito] = {}         # Distrito DB
tarifa_db: Dict[str, Tarifas] = {}            # Tarifas DB
tickets_db: Dict[str, Ticket] = {}            # Tickets DB

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

def update_cochera_rating(cochera_id: str) -> None:
    """Update the average rating for a cochera"""
    # This function is no longer relevant since disponibilidad_db no longer stores reviews.
    pass

def update_disponibilidad(cochera_id: str, available: bool) -> None:
    """Update the availability status of a cochera."""
    if cochera_id in disponibilidad_db:
        disponibilidad_db[cochera_id].status = CocheraStatus.available if available else CocheraStatus.reserved
        disponibilidad_db[cochera_id].start_time = datetime.datetime.now()
        disponibilidad_db[cochera_id].end_time = None
        # Update cochera status in cocheras_db as well
        cocheras_db[cochera_id].status = CocheraStatus.available if available else CocheraStatus.reserved
    else:
        raise ValueError(f"Cochera with ID {cochera_id} does not exist.")

def init_sample_data():
    """Initialize sample data for development and testing"""
    # Clear existing data
    users_db.clear()
    autos_db.clear()
    cocheras_db.clear()
    reservas_db.clear()
    disponibilidad_db.clear()
    distrito_db.clear()
    tarifa_db.clear()
    tickets_db.clear()
    
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
    
    # Create sample districts
    distrito_db["1"] = Distrito(id="1", name="Chorrillos")
    distrito_db["2"] = Distrito(id="2", name="Miraflores")
    distrito_db["3"] = Distrito(id="3", name="Surco")
    distrito_db["4"] = Distrito(id="4", name="Barranco")
    
    # Create sample cocheras
    locations = ["Chorrillos", "Miraflores", "Surco", "Barranco"]
    prices = [5.0, 7.5, 10.0, 15.0]  # Prices per hour
    
    cochera_ids = []
    for i in range(len(locations)):
        cochera_id = generate_id()
        cochera_ids.append(cochera_id)
        cocheras_db[cochera_id] = Cochera(
            id=cochera_id,
            location=locations[i],
            price=prices[i],
            status=CocheraStatus.available,
            size="Standard" if i < 2 else "Large"
        )
        
        # Initialize availability for each cochera
        disponibilidad_db[cochera_id] = Disponibilidad(
            cochera_id=cochera_id,
            start_time=datetime.datetime.now(),
            end_time=None,
            status=CocheraStatus.available
        )
    
    # Create a sample reservation
    reserva_id = generate_id()
    start_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(hours=3)
    
    reservas_db[reserva_id] = Reserva(
        id=reserva_id,
        cochera_id=cochera_ids[0],
        user_id=client_id,
        start_time=start_time,
        end_time=end_time,
        status=ReservationStatus.active,
        payment_status=PaymentStatus.pending
    )
    
    # Update cochera status
    cocheras_db[cochera_ids[0]].status = CocheraStatus.reserved
    disponibilidad_db[cochera_ids[0]].status = CocheraStatus.reserved
    
    # Create sample tariffs
    tarifa_db[cochera_ids[0]] = Tarifas(
        cochera_id=cochera_ids[0],
        tarifa_hora=5.0,
        tarifa_dia=30.0,
        tarifa_semana=150.0,
        tarifa_mes=500.0
    )
    
    # Create sample tickets
    ticket_id = generate_id()
    tickets_db[ticket_id] = Ticket(
        id=ticket_id,
        reserva_id=reserva_id,
        cochera_id=cochera_ids[0],
        user_id=client_id,
        start_time=start_time,
        end_time=end_time,
        status=ReservationStatus.active
    )
    
    return {
        "owner_id": owner_id,
        "client_id": client_id,
        "cochera_ids": cochera_ids,
        "reserva_id": reserva_id,
        "ticket_id": ticket_id
    }
