from pydantic import BaseModel, EmailStr
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

# Users
class UserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    saldo: float
    monedero_ahorro: float

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    saldo: float
    monedero_ahorro: float

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
    product_id: int
    quantity: int

# User
class UserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    saldo: float
    monedero_ahorro: float