from fastapi import APIRouter
from Lab1.services.wallet_service import add_funds, get_balance
from Lab1.api.schemas import WalletRequest, WalletResponse

router = APIRouter()

@router.post("/wallet", response_model=WalletResponse)
def add_wallet_funds(wallet: WalletRequest):
    return add_funds(wallet)

@router.get("/wallet", response_model=WalletResponse)
def get_wallet_balance():
    return get_balance()