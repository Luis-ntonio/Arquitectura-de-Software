from fastapi import APIRouter, HTTPException
from database import users_db
from models import UserCreate, UserResponse

router = APIRouter()

@router.get("/")
def list_users():
    return list(users_db.values())

@router.post("/")
def create_user(user: UserCreate):
    if user.username in [u["username"] for u in users_db.values()]:
        raise HTTPException(status_code=400, detail="Username already exists")
    user_id = f"user_{len(users_db) + 1}"
    users_db[user_id] = user.dict()
    return {"id": user_id, **user.dict()}