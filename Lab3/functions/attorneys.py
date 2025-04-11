from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Attorney
from database import get_all_attorneys, get_attorney, create_attorney, update_attorney, delete_attorney, DatabaseError

router = APIRouter()


@router.get("/", response_model=List[Attorney])
async def read_attorneys():
    return await get_all_attorneys()


@router.get("/{attorney_id}", response_model=Attorney)
async def read_attorney(attorney_id: str):
    try:
        attorney = await get_attorney(attorney_id)
        if not attorney:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attorney not found")
        return attorney
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=Attorney, status_code=status.HTTP_201_CREATED)
async def create_new_attorney(attorney: Attorney):
    try:
        return await create_attorney(attorney.name, attorney.email, attorney.phone, attorney.type)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{attorney_id}", response_model=Attorney)
async def update_existing_attorney(attorney_id: str, attorney: Attorney):
    try:
        updated_attorney = await update_attorney(attorney_id, attorney.name, attorney.email, attorney.phone,
                                                 attorney.type)
        if not updated_attorney:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attorney not found")
        return updated_attorney
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{attorney_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_attorney(attorney_id: str):
    try:
        success = await delete_attorney(attorney_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attorney not found")
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))