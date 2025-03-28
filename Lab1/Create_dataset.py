import psycopg2
import os
import dotenv

dotenv.load_dotenv()

def create_table(conn, embedding_dim=384):
    """
    Crea tabla para almacenar el entorno de datos.

    Args:
        conn: Conexión a la base de datos.

    Returns:
        None
    """
    cur = conn.cursor()
    # Crear la tabla para almacenar los chunks y sus embeddings
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS chunks (
            id SERIAL PRIMARY KEY,
            text TEXT,
            embedding VECTOR({embedding_dim})
        );
    """)
    conn.commit()
    cur.close()

def create_conn():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
    )
    return conn