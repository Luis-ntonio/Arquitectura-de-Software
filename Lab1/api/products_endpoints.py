from fastapi import APIRouter
from Lab1.services.product_service import list_products, add_product, update_product
from Lab1.api.schemas import ProductRequest, ProductResponse

router = APIRouter()

@router.get("/products", response_model=list[ProductResponse])
def get_products():
    return list_products()

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductRequest):
    return add_product(product)

@router.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, cantidad: int):
    return update_product(product_id, cantidad)