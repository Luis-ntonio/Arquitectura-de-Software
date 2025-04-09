from fastapi import APIRouter, HTTPException, Body, status
from typing import Dict, Any, List, Optional
from datetime import datetime

from database import get_user_by_username, reservas_db, cocheras_db, generate_id
from models import ReservaCreate, ReservaUpdate, ReservaResponse

router = APIRouter()

@router.get("/", response_model=List[ReservaResponse])
def list_reservations(
    username: str = Body(...),  # pass username directly
    reservaStatus: Optional[str] = None
):
    """
    List reservations for the current user.
    Owners see reservations for their parking spots.
    Clients see their own reservations.
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    result = []
    if current_user["role"] == "client":
        # Return client's reservations
        for reserva_id, data in reservas_db.items():
            if data["user_id"] == current_user["user_id"]:
                if reservaStatus and data["status"] != reservaStatus:
                    continue
                result.append({"reserva_id": reserva_id, **data})
    else:
        # Return reservations for owner's parking spots
        owned_cocheras = [
            c_id for c_id, data in cocheras_db.items() 
            if data["owner_id"] == current_user["user_id"]
        ]
        for reserva_id, data in reservas_db.items():
            if data["cochera_id"] in owned_cocheras:
                if reservaStatus and data["status"] != reservaStatus:
                    continue
                result.append({"reserva_id": reserva_id, **data})
    
    return result

@router.get("/{reserva_id}", response_model=ReservaResponse)
def get_reservation(
    reserva_id: str,
    username: str = Body(...)
):
    """
    Get details for a specific reservation.
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if reserva_id not in reservas_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    
    reserva = reservas_db[reserva_id]
    
    # Check permissions
    if current_user["role"] == "client" and reserva["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this reservation"
        )
    
    if current_user["role"] == "owner":
        # Verify the reservation belongs to one of the owner's parking spots
        cochera = cocheras_db.get(reserva["cochera_id"])
        if not cochera or cochera["owner_id"] != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this reservation"
            )
    
    return {"reserva_id": reserva_id, **reserva}

@router.post("/", response_model=ReservaResponse)
def create_reservation(
    reserva: ReservaCreate,
    username: str = Body(...)
):
    """
    Create a new reservation (only for clients).
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients can create reservations"
        )
    
    if reserva.cochera_id not in cocheras_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Parking spot not found"
        )
    
    # Check if the parking spot is available
    if cocheras_db[reserva.cochera_id]["status"] != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Parking spot is not available"
        )
    
    # Parse start and end times
    try:
        start_time = datetime.fromisoformat(reserva.start_time)
        end_time = datetime.fromisoformat(reserva.end_time)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
        )
    
    if start_time < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Start time must be in the future"
        )
    
    # Calculate duration and total price
    duration_hours = (end_time - start_time).total_seconds() / 3600
    price_total = cocheras_db[reserva.cochera_id]["price"] * duration_hours
    
    # Create the reservation
    reserva_id = generate_id()
    created_at = datetime.now().isoformat()
    reservas_db[reserva_id] = {
        "user_id": current_user["user_id"],
        "cochera_id": reserva.cochera_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": "active",
        "created_at": created_at,
        "price_total": round(price_total, 2),
        "payment_status": "pending"
    }
    
    # Mark the parking spot as reserved
    cocheras_db[reserva.cochera_id]["status"] = "reserved"
    
    return {"reserva_id": reserva_id, **reservas_db[reserva_id]}

@router.patch("/{reserva_id}", response_model=ReservaResponse)
def update_reservation(
    reserva_id: str,
    update_data: ReservaUpdate,
    username: str = Body(...)
):
    """
    Update a reservation.
    Clients can cancel their reservations.
    Owners can mark reservations as completed.
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if reserva_id not in reservas_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    
    reserva = reservas_db[reserva_id]
    cochera_id = reserva["cochera_id"]
    
    is_owner = False
    if current_user["role"] == "owner":
        cochera = cocheras_db.get(cochera_id)
        if cochera and cochera["owner_id"] == current_user["user_id"]:
            is_owner = True
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this reservation"
            )
    elif current_user["role"] == "client" and reserva["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this reservation"
        )
    
    if update_data.status is not None:
        # Clients are allowed only to cancel their reservations
        if current_user["role"] == "client" and update_data.status != "cancelled":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Clients can only cancel reservations"
            )
        
        reservas_db[reserva_id]["status"] = update_data.status
        
        # Free the parking spot if the reservation is cancelled or completed
        if update_data.status in ["cancelled", "completed"]:
            if cochera_id in cocheras_db:
                cocheras_db[cochera_id]["status"] = "available"
    
    if update_data.payment_status is not None and is_owner:
        reservas_db[reserva_id]["payment_status"] = update_data.payment_status
    
    return {"reserva_id": reserva_id, **reservas_db[reserva_id]}

@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reserva_id: str,
    username: str = Body(...)
):
    """
    Delete a reservation
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if reserva_id not in reservas_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    
    reserva = reservas_db[reserva_id]
    cochera_id = reserva["cochera_id"]
    
    del reservas_db[reserva_id]
    
    if cochera_id in cocheras_db:
        cocheras_db[cochera_id]["status"] = "available"
