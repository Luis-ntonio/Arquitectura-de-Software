from fastapi import APIRouter
from Lab1.services.wallet_service import add_funds, get_balance, discount_wallet
from Lab1.api.schemas import WalletRequest, WalletResponse

router = APIRouter()

@router.post("/wallet/{user_id}", response_model=WalletResponse)
def add_wallet_funds(amount: int, user_id: int):
    return add_funds(amount, user_id=user_id)

@router.get("/wallet/{user_id}", response_model=WalletResponse)
def get_wallet_balance(user_id: int):
    return get_balance(user_id=user_id)

@router.patch("/wallet/{user_id}", response_model=WalletResponse)
def discount_wallet(amount: float, user_id: int):
    return discount_wallet(amount, user_id=user_id)