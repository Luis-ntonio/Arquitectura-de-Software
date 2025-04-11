from fastapi import APIRouter, HTTPException, status
from typing import List
from database import get_all_attorneys, get_attorney, create_attorney  # Import your DB functions
from models import Attorney

router = APIRouter()

@router.get("/", response_model=List[Attorney])
async def read_attorneys():
    return await get_all_attorneys()

@router.get("/{attorney_id}", response_model=Attorney)
async def read_attorney(attorney_id: str):
    attorney = await get_attorney(attorney_id)
    if not attorney:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attorney not found")
    return attorney

@router.post("/", response_model=Attorney, status_code=status.HTTP_201_CREATED)
async def create_new_attorney(attorney: Attorney):
    # Add validation or business logic here if needed
    return await create_attorney(attorney)
