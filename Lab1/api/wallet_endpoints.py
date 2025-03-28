from fastapi import APIRouter
from services.wallet_service import add_funds, get_balance, discount_wallet_by_user_id

router = APIRouter()

@router.post("/wallet/{user_id}")
def add_wallet_funds(amount: int, user_id: int):
    return add_funds(amount, user_id=user_id)

@router.get("/wallet/{user_id}")
def get_wallet_balance(user_id: int):
    return get_balance(user_id=user_id)

@router.patch("/wallet/{user_id}")
def discount_wallet(amount: float, user_id: int):
    return discount_wallet_by_user_id(amount, user_id=user_id)