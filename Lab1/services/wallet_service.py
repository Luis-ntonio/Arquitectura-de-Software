from Lab1.database.connection import get_connection

def add_funds(amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET saldo = saldo + %s
        WHERE id = 1 RETURNING saldo;
    """, (amount,))
    new_balance = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"saldo": new_balance}

def get_balance():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT saldo FROM users WHERE id = 1;")
    balance = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"saldo": balance}

def discount_wallet(amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET saldo = saldo - %s
        WHERE id = 1 RETURNING saldo;
    """, (amount,))
    new_balance = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"saldo": new_balance}