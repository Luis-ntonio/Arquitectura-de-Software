from database.connection import get_connection

def add_funds(amount, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE users
        SET saldo = saldo + %s
        WHERE id = {user_id} RETURNING saldo;
    """, (amount,))
    new_balance = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"saldo": new_balance}

def get_balance(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT saldo FROM users WHERE id = {user_id};")
        balance = cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
    return {"saldo": balance}

def discount_wallet_by_user_id(amount, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET saldo = saldo - %s
        WHERE id = %s RETURNING saldo;
    """, (amount, user_id))
    new_balance = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"saldo": new_balance}