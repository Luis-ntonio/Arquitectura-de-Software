from pydantic import BaseModel
from datetime import datetime

# Products
class ProductRequest(BaseModel):
    product_name: str
    quantity: int
    price: float

class ProductResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    price: float
    created_at: datetime

# Stores (Tiendas)
class StoreRequest(BaseModel):
    nombre: str
    direccion: str

class StoreResponse(BaseModel):
    id: int
    nombre: str
    direccion: str

# Cart (Carrito)
class CartRequest(BaseModel):
    user_id: int

class CartResponse(BaseModel):
    user_id: int

class CartItemRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

# User
class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    saldo: float
    monedero_ahorro: float
