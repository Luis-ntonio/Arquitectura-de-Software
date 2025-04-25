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

- Docker y Docker Compose
- (Opcional) Python 3.11+ si deseas ejecutar servicios fuera de Docker

---

### Instalación y Ejecución

#### 1. Navega al directorio del proyecto

```bash
cd Lab5-microservices
```

#### 2. Arranca todos los servicios con Docker Compose

```bash
docker-compose down -v
docker-compose up --build
```

Esto levantará todos los microservicios y RabbitMQ definidos en el `docker-compose.yml` en contenedores separados.

#### 3. Simula el flujo de negocio ejecutando el script principal (En otra terminal):

```bash
docker-compose exec user_service python main.py
```
Verás los mensajes de los servicios y la simulación del flujo de negocio (registro, login, listado de productos, creación de pedido, etc.).

### Notas

## Comunicación entre servicios

- Los servicios se comunican entre sí a través de HTTP usando los endpoints definidos en cada servicio.
- El Event Bus (RabbitMQ) se utiliza para enviar eventos entre servicios.

## Arquitectura Física

- Cada servicio es un microservicio independiente.
- Comunicación asíncrona mediante RabbitMQ.
- Fácilmente escalable y mantenible.
