from fastapi import APIRouter, HTTPException
from database import cases_db

router = APIRouter()

VALID_STATUS_TRANSITIONS = {
    "open": ["in_progress", "closed"],
    "in_progress": ["closed"],
    "closed": []
}

@router.patch("/{case_id}")
def update_status(case_id: str, status: str):
    """
    Update the status of a case with validation for allowed transitions.
    """
    if case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Case not found")

    current_status = cases_db[case_id]["status"]
    if status not in VALID_STATUS_TRANSITIONS.get(current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from '{current_status}' to '{status}'."
        )

    cases_db[case_id]["status"] = status
    return {"case_id": case_id, "status": status}