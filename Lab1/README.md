# Análisis e Implementación de una Arquitectura de Software
Este proyecto tiene como objetivo analizar e implementar una arquitectura de software eficiente y escalable propuesta para representar el funcionamiento de [Inkafarma](https://www.inkafarma.pe), aplicando principios de diseño y buenas prácticas de desarrollo.

## Descripción de la Arquitectura

En esta sección se describe la arquitectura utilizada, incluyendo sus componentes principales y cómo interactúan entre sí:

### Componentes Principales

1. **Interaccion inicial del usuario**: Se propone que el usuario pueda interactuar de inicio con tres rutas:
- Register: El usuario podra registrarse en caso no tener una cuenta activa
- Login: el usuario va a poder iniciar sesion con su cuenta creada
- Free access: en caso no desee, el usuario podra ingresar a la plataforma en condicion de invitado con opcion a visualizar mas no comprar productos.
2. **Compra de productos**: Los productos van a poder ser consultados para visualizar disponibilidad de inventario. A su vez, el usuario podra consultar promociones de los productos y ver el estado de su billetera.
3. **Farmacias**: Se podra ver promociones dependiendo de la farmacia, tambien el delivery dependera de la geolocalizacion de las tiendas con productos disponibles.
4. **Carrito de compras**: En el carrito de compras se visualizara todos los productos agregados para comprar, tambien se podra seleccionar el metodo de pago e interactuara con el monedero del ahorro.
5. **Bot de soporte**: En caso el usuario requiera, se tiene un bot potenciado con IA para apoyar al usuario
6. **Admin**: Los trabajadores al iniciar sesion se le podra presentar una interfaz diferente con acceso a INventarios, campaigns, tiendas, blogs y datos para analisis.

### Diagrama de la Arquitectura

![Diagrama de Arquitectura](./images/Grupo-a.pdf)

## Pros y Contras de la Arquitectura

### Pros
- **Completitud**: La arquitectura propuesta cumple detallando la mayoris de los diferentes endpoints que se requieren para cumplir con un happy path.
- **Reutilización**: Los endpoints pueden ser reutilizados en otros proyectos.

### Contras
- **Faltan endpoints**: No se cuenta con endpoints para el login 
- **Desconocimiento de Tablas BD**: No se comprende en totalidad la estrutura de las Bases de datos, las tablas que son contenidas por estas.
- **Sobrecarga**: En proyectos pequeños, puede ser excesivo implementar una arquitectura compleja.
- **No es escalable**: La arquitectura no cuenta con balanceadores de cargas entre otras cosas que complicarian la escalabilidad de datos.
## Cómo Ejecutar el Proyecto

1. Clonar el repositorio.
2. Instalar las dependencias necesarias.
3. Ejecutar el proyecto utilizando el comando correspondiente.

```bash
# Ejemplo de comandos
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
<COMANDO_PARA_EJECUTAR>