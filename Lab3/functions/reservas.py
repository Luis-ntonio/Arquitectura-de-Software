from fastapi import APIRouter, HTTPException, Body, status
from typing import List, Optional
from datetime import datetime

from database import get_user_by_username, reservas_db, cocheras_db, generate_id
from models import ReservaCreate, ReservaUpdate, ReservaResponse, ReservationStatus, CocheraStatus, PaymentStatus, Reserva

router = APIRouter()

@router.get("/", response_model=List[ReservaResponse])
def list_reservations(
    username: str = Body(...),
    reservaStatus: Optional[ReservationStatus] = None
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
        for reserva in reservas_db.values():
            if reserva.user_id == current_user["user_id"]:
                if reservaStatus and reserva.status != reservaStatus:
                    continue
                result.append(reserva)
    else:
        owned_cocheras = [
            cochera_id for cochera_id, cochera in cocheras_db.items()
            if cochera.owner_id == current_user["user_id"]
        ]
        for reserva in reservas_db.values():
            if reserva.cochera_id in owned_cocheras:
                if reservaStatus and reserva.status != reservaStatus:
                    continue
                result.append(reserva)
    
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
    
    reserva = reservas_db.get(reserva_id)
    if not reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    
    if current_user["role"] == "client" and reserva.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this reservation"
        )
    
    if current_user["role"] == "owner":
        cochera = cocheras_db.get(reserva.cochera_id)
        if not cochera or cochera.owner_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this reservation"
            )
    
    return reserva

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
    
    cochera = cocheras_db.get(reserva.cochera_id)
    if not cochera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking spot not found"
        )
    
    if cochera.status != CocheraStatus.available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parking spot is not available"
        )
    
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
    
    duration_hours = (end_time - start_time).total_seconds() / 3600
    price_total = cochera.price * duration_hours
    
    reserva_id = generate_id()
    new_reserva = Reserva(
        id=reserva_id,
        cochera_id=reserva.cochera_id,
        user_id=current_user["user_id"],
        start_time=start_time,
        end_time=end_time,
        status=ReservationStatus.active,
        payment_status=PaymentStatus.pending
    )
    reservas_db[reserva_id] = new_reserva
    
    cochera.status = CocheraStatus.reserved
    
    return new_reserva

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
    
    reserva = reservas_db.get(reserva_id)
    if not reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    
    cochera = cocheras_db.get(reserva.cochera_id)
    if current_user["role"] == "owner" and cochera.owner_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this reservation"
        )
    elif current_user["role"] == "client" and reserva.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this reservation"
        )
    
    if update_data.status:
        if current_user["role"] == "client" and update_data.status != ReservationStatus.cancelled:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Clients can only cancel reservations"
            )
        reserva.status = update_data.status
        if update_data.status in [ReservationStatus.cancelled, ReservationStatus.completed]:
            cochera.status = CocheraStatus.available
    
    if update_data.payment_status and current_user["role"] == "owner":
        reserva.payment_status = update_data.payment_status
    
    return reserva

@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reserva_id: str,
    username: str = Body(...)
):
    """
    Delete a reservation.
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    reserva = reservas_db.get(reserva_id)
    if not reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    
    cochera = cocheras_db.get(reserva.cochera_id)
    if cochera:
        cochera.status = CocheraStatus.available
    
    del reservas_db[reserva_id]
