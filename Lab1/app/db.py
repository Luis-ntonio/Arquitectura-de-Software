import psycopg2
from psycopg2 import sql
import os

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "inkafarma"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "admin"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            monedero_ahorro FLOAT NOT NULL,
            saldo FLOAT NOT NULL
        )
""")
    
    conn.commit()
    cur.close()
    conn.close()
