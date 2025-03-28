from fastapi import APIRouter
from Lab1.services.cart_service import add_to_cart, get_cart, delete_all_cart
from Lab1.api.schemas import CartRequest, CartResponse, CartItemRequest

router = APIRouter()

@router.post("/cart", response_model=CartResponse)
def add_item_to_cart(item: CartItemRequest):
    return add_to_cart(item)

@router.get("/cart/{user_id}", response_model=CartResponse)
def get_cart_items(user_id: int):
    return get_cart(user_id)

@router.delete("/cart/{user_id}")
def empty_cart(user_id: int):
    return delete_all_cart(user_id)