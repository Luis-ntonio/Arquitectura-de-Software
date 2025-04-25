# Arquitectura de Microservicios con Event Bus (RabbitMQ)

### Descripción:
Esta demostración implementa una arquitectura de microservicios simple, comunicados a través de un Event Bus, para simular el flujo de importación y compra de productos desde USA a Perú.

---

### Servicios Implementados

- **User Service:** Registro y login de usuarios (`services/user_services.py`)
- **Product Service:** Listado de productos (`services/product_service.py`)
- **Order Service:** Creación de pedidos y emisión de eventos (`services/order_service.py`)
- **Payment Service:** Procesamiento de pagos (`services/payment_service.py`)
- **Notification Service:** Escucha eventos y simula notificaciones (`services/notification_service.py`)
- **Event Bus:** Comunicación asíncrona entre servicios (`event_bus/producer.py`, `event_bus/consumer.py`)

---

### Requisitos Previos

- Python 3.11+
- RabbitMQ (puede correr en Docker)

---

### Instalación

```bash
pip install -r requirements.txt
```

Iniciar RabbitMQ con Docker:

```bash
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq:3
```

---

  ### Ejecución de los Servicios

  Ejecutar cada microservicio en diferentes terminales para que estén disponibles
  para la comunicación.

### Ejecución de los Servicios

En diferentes terminales, ejecutar:

```bash
python services/user_services.py
python services/product_service.py
python services/order_service.py
python services/payment_service.py
python services/notification_service.py
```

---

### Simulación de Caso de Uso

Ejecutar el flujo principal con:

```bash
python main.py
```

Esto simula:

- Registro y login de usuario
- Consulta de productos
- Creación de pedido (emitiendo evento)
- Procesamiento de pago
- Recepción de notificación (impresa por `notification_service`)

---

### Arquitectura Física

- Cada servicio es un microservicio independiente.
- Comunicación asíncrona mediante RabbitMQ.
- Fácilmente escalable y mantenible.

---

### Notas

- Este es un **POC**, los datos no se persisten y la lógica es simulada.
- Puedes extender los servicios para agregar más lógica o persistencia real.

---

### ¿Listo para implementar?

¿Quieres que te genere el código de `main.py` y el bloque actualizado de `README.md` para que lo copies directamente?
```

¿Quieres que te ayude ahora con el código de `main.py` o lo dejamos listo para que lo copies al `README.md` primero?