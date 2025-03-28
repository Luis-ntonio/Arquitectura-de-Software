from Lab1.database.connection import get_connection

def update_wallet(user_id: int, amount: float, monedero_ahorro: bool):
    conn = get_connection()
    cur = conn.cursor()
    
    if not monedero_ahorro:
        cur.execute("""
            UPDATE users SET saldo = saldo - %s
            WHERE user_id = %s
            RETURNING id, saldo;
        """, (amount, user_id))
        
    else:
        cur.execute("""
            UPDATE users SET monedero_ahorro = monedero_ahorro - %s
            WHERE user_id = %s
            RETURNING id, monedero_ahorro;
        """, (amount, user_id))

    user_id, saldo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {"id": user_id, "saldo": saldo}