from fastapi import APIRouter
from Lab1.services.user_service import add_user, get_user
from schemas import UserRequest

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    return get_user(user_id)

@router.post("/users")
def add_user(user: UserRequest):
    return add_user(user)