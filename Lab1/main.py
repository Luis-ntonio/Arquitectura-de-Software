from fastapi import FastAPI
from Lab1.database.connection import get_connection
from Lab1.database.models import create_tables
from Lab1.api.cart_endpoints import router as cart_router
from Lab1.api.wallet_endpoints import router as wallet_router
from Lab1.api.products_endpoints import router as products_router
from Lab1.api.user_endpoint import router as user_router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    conn = get_connection()
    create_tables(conn)  # Cambiado para reflejar la función correcta
    conn.close()

def simulate_purchase(user_id: int):
    """
    Simula el flujo de compra de un usuario.
    """
    conn = get_connection()
    try:
        # Paso 1: Crear un usuario con saldo inicial
        print("Creando usuario...")
        add_funds(user_id, 200.0)  # Usuario con un saldo inicial de 200
        print("Usuario creado con saldo inicial de 200.")

        # Paso 2: Crear productos
        print("Creando productos...")
        create_product(product_id=1, name="Producto A", quantity=10, price=50.0)
        create_product(product_id=2, name="Producto B", quantity=5, price=30.0)
        print("Productos creados.")

        # Paso 3: Agregar productos al carrito
        print("Agregando productos al carrito...")
        add_to_cart(user_id, product_id=1, quantity=2)  # Producto 1, cantidad 2
        add_to_cart(user_id, product_id=2, quantity=1)  # Producto 2, cantidad 1
        print("Productos agregados al carrito.")

        # Paso 4: Calcular el total del carrito
        cart_total = get_cart_total(user_id)
        print(f"Total del carrito: {cart_total}")

        # Paso 5: Verificar el saldo del usuario
        user_balance = get_balance(user_id)["saldo"]
        print(f"Saldo actual del usuario: {user_balance}")

        if user_balance < cart_total:
            print("Saldo insuficiente para realizar la compra.")
            return

        # Paso 6: Descontar el saldo del usuario
        print("Realizando la compra...")
        new_balance = discount_wallet(user_id, cart_total)["saldo"]
        print(f"Compra realizada. Nuevo saldo: {new_balance}")

        # Paso 7: Actualizar la cantidad de productos
        print("Actualizando cantidades de productos...")
        update_product_quantity(product_id=1, quantity_sold=2)
        update_product_quantity(product_id=2, quantity_sold=1)
        print("Cantidades de productos actualizadas.")

        # Paso 8: Limpiar el carrito
        clear_cart(user_id)
        print("Carrito limpiado. Compra completada.")

    except Exception as e:
        print(f"Error durante la simulación de compra: {e}")
    finally:
        conn.close()

# Ejecutar la simulación
if __name__ == "__main__":
    # Registrar los routers de los endpoints
    startup_event()
    app.include_router(cart_router, prefix="/cart", tags=["Cart"])
    app.include_router(wallet_router, prefix="/wallet", tags=["Wallet"])
    app.include_router(products_router, prefix="/products", tags=["Products"])
    simulate_purchase(user_id=1)