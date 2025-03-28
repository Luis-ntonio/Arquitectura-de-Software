from Lab1.database.connection import get_connection

def create_sale(sale):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sales (product_name, quantity, price)
        VALUES (%s, %s, %s) RETURNING id, created_at;
    """, (sale.product_name, sale.quantity, sale.price))
    sale_id, created_at = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {"id": sale_id, "created_at": created_at}