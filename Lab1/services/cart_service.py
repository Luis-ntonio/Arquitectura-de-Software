from Lab1.database.connection import get_connection

def add_to_cart(item, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cart (user_id, product_id, cantidad)
        VALUES (%s, %s);
    """, (user_id, item.product_id, item.quantity))
    conn.commit()
    cur.close()
    conn.close()
    return {"id": [item], "user_id": user_id}  # Ejemplo

def get_cart():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, product_id, quantity FROM cart;")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return {}


def delete_all_cart(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id = %s;", (user_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"text": f"Carrito del usuario {user_id} ha sido eliminado"}