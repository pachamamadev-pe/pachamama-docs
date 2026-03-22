# Pachamama API Sync (MVP / Pre-Producción)

Este microservicio se encarga de gestionar la sincronización asíncrona (offline-first) desde los dispositivos móviles (App). Está desarrollado en Java y desplegado en Heroku.

## Características del Servicio

### Stack Tecnológico

- **Lenguaje:** Java 21 
- **Framework Base:** Spring Boot 3.5.10-SNAPSHOT
- **Mensajería:** Spring Cloud Azure 6.1.0 (para Azure Service Bus)
- **Gestión de dependencias:** Maven
- **Arquitectura:** Arquitectura Hexagonal / Puertos y Adaptadores (dapter, pplication, domain)

## Integraciones del Servicio

A nivel técnico y de negocio, este servicio actúa como una capa receptora de eventos que se comunica con:
- **Colas Azure (Service Bus):** Realiza operaciones de Productor/Consumidor sobre la cola ctivities-sync-queue.
- **Base de Datos (Railway):** Persistencia en batch o asíncrona hacia la base PostgreSQL, validando y volcando el listado encolado.
- **Frontend App:** Expone endpoints REST (APP -- REST --> API2) que recibe la data de las sincronizaciones enviadas por dispositivos móviles que recobraron la conectividad.

## Despliegue / Repositorio

- **Repositorio:** pachamama-api-sync-java
- **Alojamiento:** Heroku (App: pachamama-api-sync-java)
- **CI/CD:** Completamente automatizado a través de workflows con **GitHub Actions**. Al realizarse un cambio sobre la rama main, se activa el pipeline que construye y despliega la nueva versión directamente.

## Configuración y Variables de Entorno

Para habilitar las funciones de este procesador Background/Sync, requiere de los siguientes parámetros:

**General**
- SPRING_PROFILES_ACTIVE: Perfil del aplicativo.
- PORT o SERVER_PORT: Puerto HTTP (por defecto 8081).

**Base de Datos Operativa (Railway)**
- POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD: Credenciales de PostgreSQL para persistencia e inserción post-cola.

**Base de Datos de Histórico / NoSQL (MongoDB)**
- MONGODB_URI: Cadena de conexión hacia Atlas para logs o eventos estructurados.
- MONGODB_DATABASE: Base de datos.

**Azure Service Bus (Colas de Sincronización)**
- AZURE_SERVICEBUS_NAMESPACE y AZURE_SERVICEBUS_CONNECTION_STRING: Conexión hacia la plataforma mensajera.
- ACTIVITIES_QUEUE_NAME: Nombre de la cola principal para actividades (ctivities-sync-queue).
- FOREST_UNITS_QUEUE_NAME: Nombre de la cola de sync de bosques.
- ACTIVITIES_DLQ_NAME / FOREST_UNITS_DLQ_NAME: Nombres asociados a la cola de correos/mensajes muertos (DLQ).
- AZURE_MAX_RETRIES: Número de intentos en el consumo de mensajes (Ej: 3).
