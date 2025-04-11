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
def create_cochera(id, location, price, status, size):
    return Cochera(
            id=id,
            location=location,
            price=price,
            status=status,
            size=size
        )