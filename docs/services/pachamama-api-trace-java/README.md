# Pachamama API Traceability (MVP / Pre-Producción)

Este microservicio provee la capa de lectura (Read-Model) enfocada en la trazabilidad de lotes y eventos para la Landing Page y tableros informativos. Está desarrollado en Java y desplegado en Heroku.

## Características del Servicio

### Stack Tecnológico

- **Lenguaje:** Java 21
- **Framework Base:** Quarkus 3.17.7
- **Capa Exposición REST:** quarkus-rest-jackson
- **Capa Base de Datos:** MongoDB con Panache (quarkus-mongodb-panache)
- **Gestión de dependencias:** Maven

## Integraciones del Servicio

A nivel de arquitectura funciona bajo un modelo CQRS leyendo de una base no-relacional paralela:
- **Base de Datos (MongoDB Atlas):** Lectura exclusiva de la colección pachamama_traceability_readmodel_dev. (Los datos aquí son inyectados previamente de forma reactiva por Service Bus y Funciones de Azure).
- **Frontend Consumidores:** 
  - La Landing Page (o clientes externos LANDING -- REST --> API4) consume esta API directamente para pintar resúmenes de impacto y tracking de los lotes.

## Despliegue / Repositorio

- **Repositorio:** pachamama-api-trace-java
- **Alojamiento:** Heroku (App: pachamama-api-trace-java)
- **CI/CD:** El despliegue de esta aplicación está completamente automatizado a través de workflows con **GitHub Actions**. Al realizarse un cambio sobre la rama main, se activa el pipeline.

## Configuración y Variables de Entorno

Este servicio basado en Quarkus orienta su carga al modelo de lectura geoespacial / de trazabilidad. Requiere los siguientes valores:

**General**
- PORT o QUARKUS_HTTP_PORT: Puerto HTTP del servidor (8089).

**Base de Datos NoSQL (MongoDB Atlas)**
- MONGODB_URI: URi de conexión (Protocolo SRV) con parámetros de retry y autenticación.
- MONGODB_DATABASE: Nombre de la base de datos (ej. pachamama_traceability_readmodel_dev).

**Seguridad Genérica y JWT (MicroProfile OpenID)**
- JWT_DURATION_SECONDS: Expiración de tokens delegados.
- JWT_ISSUER: Emisor (https://pachamama.app).
- JWT_PRIVATE_KEY y JWT_PUBLIC_KEY: Par de llaves para firma y validación de tokens de MicroProfile JWT.
- BASIC_AUTH_USERNAME / BASIC_AUTH_PASSWORD: Credenciales básicas usadas por clientes o admins directos.
