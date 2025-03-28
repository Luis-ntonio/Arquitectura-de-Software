from fastapi import APIRouter
from services.user_service import get_user_by_id, create_user
from .schemas import UserRequest

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    return get_user_by_id(user_id)

@router.post("/users")
def add_user(user: UserRequest):
    return create_user(user)