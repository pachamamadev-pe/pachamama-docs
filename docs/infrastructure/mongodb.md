# Plataforma MongoDB Atlas (MVP / Pre-Producción)

**MongoDB Atlas** se utiliza como el clúster gestionado de base de datos NoSQL. Es crucial para el modelo de lectura rápida y persistencia de eventos sin esquema rígido.

## Cuentas

- **Cuenta Principal:** `[Pendiente de definir]`
- **Uso:** Alojamiento de Bases de Datos NoSQL.

## Integraciones y Configuraciones Cloud

### Colecciones y Bases de datos utilizadas

- **`pachamama_notifications` (Base de datos):** Utilizada por el microservicio `pachamama-api-notifications-java` para persistir un historial o registro de las notificaciones enviadas y alertas de la plataforma.
- **`pachamama_traceability_readmodel_dev` (Colección):** Colección principal adaptada para ser consumida como *ReadModel* bajo un enfoque arquitectónico CQRS. Se llena asíncronamente y es consultada en exclusiva modo-lectura por la `pachamama-api-trace-java`.