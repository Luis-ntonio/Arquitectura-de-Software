from fastapi import APIRouter
from Lab1.services.wallet_service import add_funds, get_balance, discount_wallet
from Lab1.api.schemas import WalletRequest, WalletResponse

router = APIRouter()

@router.post("/wallet")
def add_wallet_funds(amount: int):
    return add_funds(amount)

@router.get("/wallet")
def get_wallet_balance():
    return get_balance()

@router.patch("/wallet")
def discount_wallet(amount: float):
    return discount_wallet(amount)