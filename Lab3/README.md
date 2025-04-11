# Sistema de Gestión de Casos Legales - Demostración

Este proyecto demuestra una arquitectura simplificada para un Sistema de Gestión de Casos Legales y almacenamiento de datos en memoria para simular interacciones con una base de datos.

## Ejecutando main.py

Esta demostración está configurada para ejecutarse directamente como un script de Python sin necesidad de iniciar un servidor FastAPI separado.

1.  **Asegúrese de tener Python 3.11 o una versión compatible instalada.**
2.  **Instale las dependencias:** Puede instalarlas usando pip:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecute el script `main.py`:**
    ```bash
    python main.py
    ```
4.  **Observe la salida:** El script realizará lo siguiente:
    * Inicializará datos de casos de ejemplo.
    * Imprimirá la lista inicial de casos (simulando una operación de "Listar Casos").
    * Simulará la creación de un nuevo caso llamando a la función `create_new_case` del enrutador de `cases`.
    * Imprimirá la lista de casos después de que se cree el nuevo.
    * Simulará la eliminación del caso recién creado llamando a la función `delete_existing_case` del enrutador de `cases`.
    * Imprimirá la lista de casos después de la eliminación.

## Demostración de la Arquitectura

El script `main.py` demuestra los siguientes componentes arquitectónicos:

* **Interacción del Usuario (Simulada):** La función `demonstrate_case_flow` en `main.py` actúa como un usuario o cliente simulado que interactúa con el sistema.
* **Endpoints de la API (Enrutadores):** El archivo `functions/cases.py` define endpoints de la API (utilizando `APIRouter` de FastAPI) para la gestión de casos (por ejemplo, crear, leer, eliminar). El script `main.py` llama directamente a estas funciones del enrutador.
* **Servicio de Información de Casos (Simulado):** Las funciones del enrutador en `functions/cases.py` llaman a las funciones en `database.py` para realizar operaciones CRUD en el `cases_db` en memoria. Esto simula un servicio dedicado para manejar los datos de los casos.
* **BD (Base de Datos - Simulada):** El archivo `database.py` utiliza diccionarios de Python (`cases_db`) para simular una base de datos para almacenar la información de los casos.

Esta demostración simplificada muestra el flujo de datos y control entre estos componentes para operaciones básicas de gestión de casos. En una aplicación del mundo real, se accedería a los endpoints de la API a través de solicitudes HTTP, y `database.py` interactuaría con un sistema de base de datos real.

## `optional.sql`

El archivo `optional.sql` en el directorio `bd` contiene un esquema SQL simplificado para las tablas de la base de datos. Este archivo no se utiliza activamente en esta demostración en memoria, pero proporciona una estructura potencial para una base de datos persistente.

## Modelos Pydantic

El archivo `models.py` define modelos Pydantic (`Attorney`, `Client`, `Cases`, `Attachment`). Estos modelos se utilizan para:

* **Validación de Datos:** Asegurar que los datos se ajusten a la estructura y tipos esperados.
* **Serialización de Datos:** Convertir objetos de Python a JSON para respuestas de la API (en una aplicación FastAPI completa).
* **Tipado Estático:** Mejorar la legibilidad y el mantenimiento del código.