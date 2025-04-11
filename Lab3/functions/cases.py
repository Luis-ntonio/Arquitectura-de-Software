from fastapi import APIRouter, HTTPException
from database import cases_db
from models import Case

router = APIRouter()

@router.get("/")
def list_cases():
    return list(cases_db.values())

@router.post("/")
def create_case(case: Case):
    if case.id in cases_db:
        raise HTTPException(status_code=400, detail="Case already exists")
    cases_db[case.id] = case.dict()
    return case