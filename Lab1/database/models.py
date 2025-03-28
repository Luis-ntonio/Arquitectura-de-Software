from connection import get_connection

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            product_name TEXT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            saldo FLOAT NOT NULL,
            monedero_ahorro FLOAT NOT NULL,
        );
    """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS tiendas (
            id SERIAL PRYMARY KEY,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
        );
    """)

    conn.commit()
    cur.close()
    conn.close()