from Lab1.database.connection import get_connection

def update_product(product_id, cantidad):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE productos
        SET quantity = quantity - %s
        WHERE id = %s
    """, (cantidad, product_id))