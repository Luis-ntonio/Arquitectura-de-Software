from Lab1.database.connection import get_connection

def add_to_cart(item):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cart (product_id, quantity)
        VALUES (%s, %s);
    """, (item.product_id, item.quantity))
    conn.commit()
    cur.close()
    conn.close()
    return {"items": [item], "total_price": item.quantity * 10.0}  # Ejemplo

def get_cart():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT product_id, quantity FROM cart;")
    items = cur.fetchall()
    cur.close()
    conn.close()
    return {"items": items, "total_price": sum(item[1] * 10.0 for item in items)}  # Ejemplo