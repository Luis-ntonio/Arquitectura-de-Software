from fastapi import APIRouter
from Lab1.services.sales_service import create_sale
from Lab1.api.schemas import SaleRequest, SaleResponse

router = APIRouter()

@router.post("/sales", response_model=SaleResponse)
def create_sale_endpoint(sale: SaleRequest):
    return create_sale(sale)