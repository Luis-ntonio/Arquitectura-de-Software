from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models import Cases
from database import get_all_cases, get_case, create_case, update_case, delete_case, DatabaseError

router = APIRouter()


@router.get("/", response_model=List[Cases])
async def read_cases():
    return await get_all_cases()


@router.get("/{case_id}", response_model=Cases)
async def read_case(case_id: str):
    try:
        case = await get_case(case_id)
        if not case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
        return case
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=Cases, status_code=status.HTTP_201_CREATED)
async def create_new_case(case: Cases):
    try:
        new_case = await create_case(case.name, case.status, case.description, case.attorney_id, case.client_id, case.attachment_id)
        return new_case  # Make sure 'new_case' has the 'id'
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{case_id}/status", response_model=Cases)
async def update_case_status_endpoint(case_id: str, status: str):
    try:
        case = await get_case(case_id)
        if not case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
        updated_case = await update_case(case_id, status=status)
        if not updated_case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
        return updated_case
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.put("/{case_id}", response_model=Cases)
async def update_case_info_endpoint(case_id: str, updated_case: Cases):
    try:
        case = await get_case(case_id)
        if not case:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
        updated_case_in_db = await update_case(
            case_id,
            name=updated_case.name,
            status=updated_case.status,
            description=updated_case.description,
            attorney_id=updated_case.attorney_id,
            client_id=updated_case.client_id,
            attachment_id=updated_case.attachment_id
        )
        if not updated_case_in_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
        return updated_case_in_db
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_case(case_id: str):
    try:
        success = await delete_case(case_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
