from fastapi import APIRouter
from Lab1.services.product_service import list_products, add_product
from Lab1.api.schemas import ProductRequest, ProductResponse

router = APIRouter()

@router.get("/products", response_model=list[ProductResponse])
def get_products():
    return list_products()

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductRequest):
    return add_product(product)