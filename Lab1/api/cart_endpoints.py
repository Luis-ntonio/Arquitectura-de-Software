from fastapi import APIRouter
from Lab1.services.cart_service import add_to_cart, get_cart
from Lab1.api.schemas import CartItemRequest, CartResponse

router = APIRouter()

@router.post("/cart", response_model=CartResponse)
def add_item_to_cart(item: CartItemRequest):
    return add_to_cart(item)

@router.get("/cart", response_model=CartResponse)
def get_cart_items():
    return get_cart()