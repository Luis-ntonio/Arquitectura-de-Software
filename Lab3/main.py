# main.py

# Importamos lo necesario de database y models
from database import (
    init_sample_data,
    users_db,
    cocheras_db,
    reservas_db,
    tickets_db,
    generate_id,
    get_user_by_username
)
from models import (
    Reserva,
    Ticket,
    CocheraStatus,
    ReservationStatus,
    PaymentStatus
)
from datetime import datetime, timedelta
import random # Para seleccionar una cochera al azar

# Por ahora, usaremos la lógica directamente o funciones de database.py

def reservar_cochera_y_generar_ticket(client_username: str):
    """
    Simula el flujo de reserva de una cochera y la generación del ticket
    para un usuario cliente específico.
    """
    print(f"--- Iniciando flujo de reserva para el usuario: {client_username} ---")

    # 1. Buscar al usuario cliente
    # En lugar de un login complejo, buscamos directamente en la DB simulada
    user_info = None
    client_id = None
    for uid, data in users_db.items():
        if data["username"] == client_username and data["role"] == "client":
            user_info = data
            client_id = uid 
            break

    if not user_info:
        print(f"Error: No se encontró al usuario cliente '{client_username}' o no tiene el rol 'client'.")
        return

    print(f"Usuario encontrado: {user_info['username']} (ID: {client_id})")

    # 2. Buscar una cochera disponible
    cocheras_disponibles = []
    for cochera_id, cochera_data in cocheras_db.items():
        # Asumiendo que cochera_data es un objeto Cochera o un dict con 'status'
        status = cochera_data.status 
        if status == CocheraStatus.available:
             # Necesitamos el ID y el objeto/dict completo
            cocheras_disponibles.append({"id": cochera_id, "data": cochera_data})

    if not cocheras_disponibles:
        print("Error: No hay cocheras disponibles en este momento.")
        return

    # 3. Seleccionar una cochera (aquí elegimos una al azar como ejemplo)
    cochera_seleccionada_info = random.choice(cocheras_disponibles)
    cochera_seleccionada_id = cochera_seleccionada_info["id"]
    cochera_seleccionada_data = cochera_seleccionada_info["data"]
    # Acceder a los atributos/claves del objeto/diccionario Cochera
    location = cochera_seleccionada_data.location
    price = cochera_seleccionada_data.price

    print(f"Cochera seleccionada: ID={cochera_seleccionada_id}, Ubicación={location}, Precio/hr={price}")

    # 4. Definir los tiempos de la reserva (ejemplo: 1 hora desde ahora)
    start_time = datetime.now() + timedelta(minutes=5) # Empezar en 5 mins
    end_time = start_time + timedelta(hours=1)       # Duración de 1 hora

    # 5. Crear la reserva 
    reserva_id = generate_id()
    nueva_reserva = Reserva(
        id=reserva_id,
        cochera_id=cochera_seleccionada_id,
        user_id=client_id,
        start_time=start_time,
        end_time=end_time,
        status=ReservationStatus.active, # O 'pending' si requiere confirmación/pago
        payment_status=PaymentStatus.pending
    )

    # 6. Guardar la reserva en la "base de datos" (diccionario)
    reservas_db[reserva_id] = nueva_reserva
    print("\n--- Reserva Creada ---")
    print(f"ID Reserva: {nueva_reserva.id}")
    print(f"Usuario: {client_username}")
    print(f"Cochera: {location} (ID: {nueva_reserva.cochera_id})")
    print(f"Inicio: {nueva_reserva.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Fin: {nueva_reserva.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Estado Reserva: {nueva_reserva.status.value}")
    print(f"Estado Pago: {nueva_reserva.payment_status.value}")


    # 7. Actualizar el estado de la cochera a 'reserved'
    # modificar el status directamente en el objeto. Si almacena dicts, necesitas
    # reemplazar el dict o actualizar la clave 'status'.
    # Si cocheras_db[cochera_seleccionada_id] es un objeto Cochera:
    try:
         cocheras_db[cochera_seleccionada_id].status = CocheraStatus.reserved
         print(f"\nEstado de la cochera {cochera_seleccionada_id} actualizado a: {CocheraStatus.reserved.value}")
    except AttributeError:
         # Si es un diccionario:
         if isinstance(cocheras_db[cochera_seleccionada_id], dict):
              cocheras_db[cochera_seleccionada_id]['status'] = CocheraStatus.reserved
              print(f"\nEstado de la cochera {cochera_seleccionada_id} actualizado a: {CocheraStatus.reserved.value}")
         else:
              print(f"Advertencia: No se pudo actualizar el estado de la cochera {cochera_seleccionada_id}.")


    # 8. Generar el Ticket
    ticket_id = generate_id()
    nuevo_ticket = Ticket(
        id=ticket_id,
        reserva_id=reserva_id,
        cochera_id=cochera_seleccionada_id,
        user_id=client_id,
        start_time=start_time, # Usar los mismos tiempos de la reserva
        end_time=end_time,
        status=nueva_reserva.status # El ticket refleja el estado inicial de la reserva
    )

    # 9. Guardar el ticket en la "base de datos" (diccionario)
    tickets_db[ticket_id] = nuevo_ticket
    print("\n--- Ticket Generado ---")
    print(f"ID Ticket: {nuevo_ticket.id}")
    print(f"Asociado a Reserva ID: {nuevo_ticket.reserva_id}")
    print(f"Detalles:")
    print(f"  Usuario: {client_username}")
    print(f"  Cochera: {location} (ID: {nuevo_ticket.cochera_id})")
    print(f"  Válido desde: {nuevo_ticket.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Válido hasta: {nuevo_ticket.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Estado: {nuevo_ticket.status.value}")

    print("\n--- Flujo de reserva completado ---")

# --- Punto de entrada principal del script ---
if __name__ == "__main__":
    print("Inicializando datos de ejemplo...")
    # Inicializamos los datos (esto llenará users_db, cocheras_db, etc.)
    init_sample_data()
    print("Datos inicializados.")

    # Imprimir estado inicial para verificar
    print("\n--- Estado Inicial ---")
    print(f"Usuarios: {len(users_db)}")
    print(f"Cocheras: {len(cocheras_db)}")
    # Contar disponibles
    disponibles_inicial = sum(1 for c in cocheras_db.values() if c.status == CocheraStatus.available)
    print(f"Cocheras Disponibles: {disponibles_inicial}")
    print(f"Reservas: {len(reservas_db)}")
    print(f"Tickets: {len(tickets_db)}")
    print("----------------------\n")


    # Ejecutamos el flujo de ejemplo para el usuario cliente de prueba
    # Asegúrate que 'parking_client' exista en init_sample_data
    reservar_cochera_y_generar_ticket(client_username="parking_client")

    # Imprimir estado final para verificar cambios
    print("\n--- Estado Final ---")
    print(f"Usuarios: {len(users_db)}")
    print(f"Cocheras: {len(cocheras_db)}")
    disponibles_final = sum(1 for c in cocheras_db.values() if c.status == CocheraStatus.available)
    print(f"Cocheras Disponibles: {disponibles_final}")
    print(f"Reservas: {len(reservas_db)}")
    # Puedes imprimir la última reserva si quieres verla
    # print("Última reserva:", list(reservas_db.values())[-1])
    print(f"Tickets: {len(tickets_db)}")
    # Puedes imprimir el último ticket
    # print("Último ticket:", list(tickets_db.values())[-1])
    print("----------------------")


