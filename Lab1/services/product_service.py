from Lab1.database.connection import get_connection

def list_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, product_name, quantity, price, created_at FROM productos;")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": p[0], "product_name": p[1], "quantity": p[2], "price": p[3], "created_at": p[4]} for p in products]

def add_product(product):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO productos (product_name, quantity, price)
        VALUES (%s, %s, %s) RETURNING id, created_at;
    """, (product.product_name, product.quantity, product.price))
    product_id, created_at = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {"id": product_id, "product_name": product.product_name, "quantity": product.quantity, "price": product.price, "created_at": created_at}

def update_product(product_id, cantidad):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE productos SET quantity = quantity - %s WHERE id = %s RETURNING id, product_name, quantity, price, created_at;
    """, (cantidad, product_id))
    product = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {"id": product[0], "product_name": product[1], "quantity": product[2], "price": product[3], "created_at": product[4]}