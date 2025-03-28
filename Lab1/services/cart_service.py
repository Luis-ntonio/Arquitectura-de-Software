from database.connection import get_connection

def add_to_cart(item):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cart (user_id, product_id, cantidad)
        VALUES (%s, %s, %s);
    """, (item.user_id, item.product_id, item.quantity))
    conn.commit()
    cur.close()
    conn.close()
    return {"item": item,}  # Ejemplo

def get_cart(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT product_id, cantidad FROM cart WHERE user_id = %s;", (user_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    return {"user_id": user_id, "items": [{"product_id": item[0], "quantity": item[1]} for item in items]}


def delete_all_cart(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE user_id = %s;", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"text": f"Carrito del usuario {user_id} ha sido eliminado"}