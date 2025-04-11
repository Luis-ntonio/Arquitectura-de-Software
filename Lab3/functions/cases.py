from fastapi import APIRouter, HTTPException, status
from typing import List
from database import get_all_cases, get_case, create_case, update_case_status, update_case_info # Import your DB functions
from models import Cases

router = APIRouter()

@router.get("/", response_model=List[Cases])
async def read_cases():
    return list(database.cases_db.values()) # Placeholder

@router.get("/{case_id}", response_model=Cases)
async def read_case(case_id: str):
    case = database.cases_db.get(case_id) # Placeholder
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return case

@router.post("/", response_model=Cases, status_code=status.HTTP_201_CREATED)
async def create_new_case(case: Cases):
    database.cases_db[case.id] = case # Placeholder
    return case

@router.put("/{case_id}/status", response_model=Cases)
async def update_case_status_endpoint(case_id: str, status: str):
    case = database.cases_db.get(case_id) # Placeholder
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    case.status = status
    return case

@router.put("/{case_id}", response_model=Cases)
async def update_case_info_endpoint(case_id: str, updated_case: Cases):
    case = database.cases_db.get(case_id) # Placeholder
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    # Update fields as needed
    case.name = updated_case.name
    case.description = updated_case.description
    case.attorney_id = updated_case.attorney_id
    case.client_id = updated_case.client_id
    case.attachment_id = updated_case.attachment_id
    return case
