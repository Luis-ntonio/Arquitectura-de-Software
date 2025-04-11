from fastapi import APIRouter, HTTPException, Body, status
from typing import Dict, Any
from database import users_db, generate_id, hash_password, verify_password, get_user_by_username
from models import UserCreate, UserResponse
from datetime import datetime

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    # Check if username already exists
    if get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken."
        )
    
    user_id = generate_id()
    created_at = datetime.now().isoformat()
    
    users_db[user_id] = {
        "username": user.username,
        "password": hash_password(user.password),
        "role": user.role,
        "email": user.email,
        "created_at": created_at
    }
    
    return {
        "user_id": user_id,
        "username": user.username,
        "role": user.role,
        "email": user.email,
        "created_at": created_at
    }

@router.post("/login", response_model=UserResponse)
def login_for_user(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True)
):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "email": user["email"],
        "created_at": user["created_at"]
    }

@router.get("/me", response_model=UserResponse)
def read_users_me(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True)
):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "email": user["email"],
        "created_at": user["created_at"]
    }
