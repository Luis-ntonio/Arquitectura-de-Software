from fastapi import APIRouter, HTTPException, status, Query, Body
from typing import Dict, Any, List, Optional
from datetime import datetime
from models import PaymentCreate, PaymentResponse
import uuid

from database import cocheras_db, reservas_db, get_user_by_username
from functions.auth import verify_password

router = APIRouter()

@router.get("/search")
def search_cocheras(
    district: Optional[str] = Query(None, description="Search by district/location"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    amenities: Optional[List[str]] = Query(None, description="Required amenities"),
    available_only: bool = Query(True, description="Show only available parking spots")
):
    """
    Enhanced search function for finding parking spots.
    """
    from database import cocheras_db
    
    result = {}
    for c_id, data in cocheras_db.items():
        # Apply filters
        if available_only and data["status"] != "available":
            continue
        if district and district.lower() not in data["location"].lower():
            continue
        if min_price is not None and data["price"] < min_price:
            continue
        if max_price is not None and data["price"] > max_price:
            continue
        if amenities:
            if not all(amenity in data["amenities"] for amenity in amenities):
                continue
        result[c_id] = data
    
    return {
        "count": len(result),
        "results": [{"cochera_id": c_id, **data} for c_id, data in result.items()]
    }

@router.post("/payment", response_model=PaymentResponse)
def process_payment(
    payment: PaymentCreate,
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True)
):
    """
    Simulated payment processing for a reservation.
    In a real app, this would integrate with a payment gateway.
    """
    # Retrieve and verify the user based on the provided username and password
    current_user = get_user_by_username(username)
    if not current_user or not verify_password(password, current_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients can make payments"
        )
    
    if payment.reserva_id not in reservas_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    reserva = reservas_db[payment.reserva_id]
    # Ensure the reservation belongs to the current user
    if reserva["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only pay for your own reservations"
        )
    
    # Check if the reservation has already been paid
    if reserva["payment_status"] == "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This reservation has already been paid"
        )
    
    reservas_db[payment.reserva_id]["payment_status"] = "completed"
    
    payment_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    
    return {
        "payment_id": payment_id,
        "reserva_id": payment.reserva_id,
        "amount": payment.amount,
        "status": "completed",
        "created_at": created_at
    }
