from fastapi import APIRouter
from services.product_service import list_products, add_product, update_product_by_id, get_product_by_id
from api.schemas import ProductRequest, ProductResponse

router = APIRouter()

@router.get("/products", response_model=list[ProductResponse])
def get_products():
    return list_products()

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_products_by_id(product_id: int):
    return get_product_by_id(product_id)

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductRequest):
    return add_product(product)

@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, cantidad: int):
    return update_product_by_id(product_id, cantidad)