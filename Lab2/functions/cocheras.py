from fastapi import APIRouter, HTTPException, status, Query, Body
from typing import Dict, Any, List, Optional
from datetime import datetime
from database import cocheras_db, reservas_db
from models import Cochera
from functions.auth import verify_password

router = APIRouter()

@router.get("/")
def list_cocheras(
    status: Optional[str] = Query(None, description="Filter by status"),
    location: Optional[str] = Query(None, description="Filter by location (partial match)"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    size: Optional[str] = Query(None, description="Filter by size")
):
    """
    List all parking spots with optional filtering.
    """
    result = []
    for cochera_id, data in cocheras_db.items():
        if status and data["status"] != status:
            continue
        if location and location.lower() not in data["location"].lower():
            continue
        if min_price is not None and data["price"] < min_price:
            continue
        if max_price is not None and data["price"] > max_price:
            continue
        if size and data["size"] != size:
            continue
        result.append({
            "cochera_id": cochera_id,
            **data
        })
    return result

@router.get("/{cochera_id}")
def get_cochera(cochera_id: str):
    if cochera_id not in cocheras_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking spot not found"
        )
    return {
        "cochera_id": cochera_id,
        **cocheras_db[cochera_id]
    }

@router.post("/")
def create_cochera(
    cochera: CocheraCreate,
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True)
):
    """
    Create a new parking spot (only for owners).
    """
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user["role"] != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can create parking spots"
        )
    
    cochera_id = generate_id()
    created_at = datetime.now().isoformat()
    cocheras_db[cochera_id] = {
        "owner_id": user["user_id"],
        "location": cochera.location,
        "price": cochera.price,
        "status": "available",
        "created_at": created_at,
        "amenities": cochera.amenities,
        "size": cochera.size,
        "rating_avg": 0.0,
        "reviews_count": 0
    }
    return {
        "cochera_id": cochera_id,
        **cocheras_db[cochera_id]
    }

@router.patch("/{cochera_id}", response_model=CocheraResponse)
def update_cochera(
    cochera_id: str,
    update_data: CocheraUpdate,
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True)
):
    """
    Update a parking spot (only for the owner of the parking spot).
    """
    if cochera_id not in cocheras_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking spot not found"
        )
    
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if cocheras_db[cochera_id]["owner_id"] != user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this parking spot"
        )
    
    if update_data.location is not None:
        cocheras_db[cochera_id]["location"] = update_data.location
    if update_data.price is not None:
        cocheras_db[cochera_id]["price"] = update_data.price
    if update_data.status is not None:
        cocheras_db[cochera_id]["status"] = update_data.status
    if update_data.amenities is not None:
        cocheras_db[cochera_id]["amenities"] = update_data.amenities
    if update_data.size is not None:
        cocheras_db[cochera_id]["size"] = update_data.size
    
    return {
        "cochera_id": cochera_id,
        **cocheras_db[cochera_id]
    }

@router.delete("/{cochera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cochera(
    cochera_id: str,
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True)
):
    """
    Delete a parking spot (only for the owner of the parking spot).
    """
    if cochera_id not in cocheras_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking spot not found"
        )
    
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if cocheras_db[cochera_id]["owner_id"] != user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this parking spot"
        )
    
    # Check if there are any active reservations
    for reserva in reservas_db.values():
        if reserva["cochera_id"] == cochera_id and reserva["status"] == "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete parking spot with active reservations"
            )
    
    del cocheras_db[cochera_id]
