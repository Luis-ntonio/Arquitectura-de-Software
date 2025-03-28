from Lab1.database.connection import get_connection

def get_user(user_id: int):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
    return result

def add_user(user):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO users (name, email, password, saldo, monedero_ahorro) VALUES (%s, %s, %s, %s, %s)", (user.name, user.email, user.password, user.saldo, user.monedero_ahorro))
        connection.commit()
    return cursor.lastrowid