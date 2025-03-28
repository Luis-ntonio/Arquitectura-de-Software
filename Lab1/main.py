from fastapi import FastAPI
from Lab1.database.connection import get_connection
from Lab1.database.models import create_tables
from Lab1.api.cart_endpoints import router as cart_router
from Lab1.api.wallet_endpoints import router as wallet_router
from Lab1.api.products_endpoints import router as products_router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    conn = get_connection()
    create_tables(conn)  # Cambiado para reflejar la función correcta
    conn.close()

# Registrar los routers de los endpoints
app.include_router(cart_router, prefix="/cart", tags=["Cart"])
app.include_router(wallet_router, prefix="/wallet", tags=["Wallet"])
app.include_router(products_router, prefix="/products", tags=["Products"])