# database.py
import uuid
import bcrypt
import datetime
from typing import Dict, Any

# Simulated tables (dictionaries)
users_db: Dict[str, Dict[str, Any]] = {}                # Autos DB
cocheras_db: Dict[str, Dict[str, Any]] = {}             # Cocheras DB
reservas_db: Dict[str, Dict[str, Any]] = {}             # Reservas DB
disponibilidad_db: Dict[str, Dict[str, Any]] = {}       # Disponibilidad DB
distrito_db: Dict[str, Dict[str, Any]] = {}             # Distrito DB
tarifa_db: Dict[str, Dict[str, Any]] = {}               # Tarifas DB
tickets_db: Dict[str, Dict[str, Any]] = {}              # Tickets DB

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
        disponibilidad_db[cochera_id]["available"] = available
        disponibilidad_db[cochera_id]["last_updated"] = datetime.datetime.now().isoformat()
        # Update cochera status in cocheras_db as well
        cocheras_db[cochera_id]["status"] = "available" if available else "reserved"
    else:
        raise ValueError(f"Cochera with ID {cochera_id} does not exist.")

def init_sample_data():
    """Initialize sample data for development and testing"""
    # Clear existing data
    users_db.clear()
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
        "username": "parking_owner",
        "password": hash_password("owner123"),
        "role": "owner",
        "created_at": datetime.datetime.now().isoformat(),
        "email": "owner@example.com"
    }
    
    users_db[client_id] = {
        "username": "parking_client",
        "password": hash_password("client123"),
        "role": "client",
        "created_at": datetime.datetime.now().isoformat(),
        "email": "client@example.com"
    }
    
    # Create sample cocheras
    locations = ["Chorrillos", "Miraflores", "Surco", "Barranco"]
    prices = [5.0, 7.5, 10.0, 15.0] # Prices per hour
    
    cochera_ids = []
    for i in range(len(locations)):
        cochera_id = generate_id()
        cochera_ids.append(cochera_id)
        cocheras_db[cochera_id] = {
            "owner_id": owner_id,
            "location": locations[i],
            "price": prices[i],
            "status": "available",
            "created_at": datetime.datetime.now().isoformat(),
            "amenities": ["Security Camera"] if i % 2 == 0 else ["Covered Parking"],
            "size": "Standard" if i < 2 else "Large",
            "rating_avg": 0.0,
            "reviews_count": 0
        }
        
        # Initialize availability for each cochera
        disponibilidad_db[cochera_id] = {
            "cochera_id": cochera_id,
            "available": True,
            "last_updated": datetime.datetime.now().isoformat()
        }
    
    # Create a sample reservation
    reserva_id = generate_id()
    start_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(hours=3)
    
    reservas_db[reserva_id] = {
        "user_id": client_id,
        "cochera_id": cochera_ids[0],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": "active",
        "created_at": datetime.datetime.now().isoformat(),
        "price_total": prices[0] * 3,  # 3 hours
        "payment_status": "pending"
    }
    
    # Update cochera status
    cocheras_db[cochera_ids[0]]["status"] = "reserved"
    disponibilidad_db[cochera_ids[0]]["available"] = False
    disponibilidad_db[cochera_ids[0]]["last_updated"] = datetime.datetime.now().isoformat()
    
    # Create sample districts
    distrito_db["1"] = {"name": "Chorrillos"}
    distrito_db["2"] = {"name": "Miraflores"}
    distrito_db["3"] = {"name": "Surco"}
    distrito_db["4"] = {"name": "Barranco"}
    
    # Create sample tariffs
    tarifa_db["1"] = {"cochera_id": cochera_ids[0], "hourly_rate": 5.0}
    tarifa_db["2"] = {"cochera_id": cochera_ids[1], "hourly_rate": 7.5}
    tarifa_db["3"] = {"cochera_id": cochera_ids[2], "hourly_rate": 10.0}
    tarifa_db["4"] = {"cochera_id": cochera_ids[3], "hourly_rate": 15.0}
    
    # Create sample tickets
    ticket_id = generate_id()
    tickets_db[ticket_id] = {
        "reserva_id": reserva_id,
        "issued_at": datetime.datetime.now().isoformat(),
        "status": "active"
    }
    
    return {
        "owner_id": owner_id,
        "client_id": client_id,
        "cochera_ids": cochera_ids,
        "reserva_id": reserva_id,
        "ticket_id": ticket_id
    }
