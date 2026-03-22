# Pachamama API Admin (MVP / Pre-Producción)

Este es el backend principal de la plataforma, encargado de la gestión operativa (comunidades, recolectores, brigadas, proyectos, etc.). Está desarrollado en Java (Spring Boot) y se encuentra alojado en Heroku. Esta configuración corresponde al entorno de pre-producción (MVP).

## Características del Servicio

### Stack Tecnológico

- **Lenguaje:** Java 21
- **Framework Base:** Spring Boot 3.3.1
- **Compilación/Gestión de dependencias:** Maven
- **Arquitectura:** Monolito / Multi-módulo (app, common, security, persistence, módulos por dominio como brigades, collectors, etc.)

## Integraciones del Servicio

Este servicio principal actúa como orquestador y se integra a nivel de negocio y técnico con:
- **Base de Datos (Railway):** Persistencia operativa leyendo/escribiendo hacia la base principal PostgreSQL (+ PostGIS).
- **Caché (Indefinido/Heroku Addon):** Utiliza Redis para cacheo de respuestas (DBR).
- **Autenticación (Firebase):** Validación de los tokens emitidos hacia el cliente móvil o web.
- **Mensajería Interna (Azure Service Bus):** Publica eventos/mensajes asíncronos en los tópicos (assigned-brigade y 	raceability-events-dev).
- **Proveedores Externos:**
  - **Twilio**: Servicio de Send/Verify OTP para autenticación.
  - **API Perú Devs**: Consultas externas de tipo DNI/RUC.
  - **Azure Storage:** Carga e indexación de archivos al Blob (admin-uploads).

## Despliegue / Repositorio

- **Repositorio:** pachamama-api-admin-java
- **Alojamiento:** Heroku (App: pachamama-api-admin-java)
- **CI/CD:** Completamente automatizado usando **GitHub Actions**. Compila y despliega en cada push/merge a la rama main hacia el Dyno usando los credenciales en secret de la cuenta dueña.

## Configuración y Variables de Entorno

Para levantar este microservicio, es necesario configurar las siguientes variables de entorno principales (basado en pplication.yaml):

**Perfil y Servidor**
- SPRING_PROFILES_ACTIVE: Perfil activo (ej. dev, local, prod).
- PORT o SERVER_PORT: Puerto HTTP.

**Base de Datos (Railway)**
- POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD: Parámetros de conexión PostgreSQL.

**Caché (Redis)**
- REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_PASSWORD: Credenciales Redis (alojado en Azure/Redislabs).

**Integraciones de Infraestructura (Azure)**
- AZURE_STORAGE_ACCOUNT_NAME y AZURE_STORAGE_ACCOUNT_KEY: Credenciales para Blob Storage.
- AZURE_STORAGE_CONTAINER: Contenedor (ej. dmin-uploads).
- SERVICEBUS_ENABLED: Activar integración.
- AZURE_SERVICEBUS_CONNECTION_STRING: Cadena de conexión Service Bus.

**Identidad y Seguridad**
- FIREBASE_PROJECT_ID: ID del proyecto (ej. pachamama-mvp).
- FIREBASE_SERVICE_ACCOUNT_FILE: Ruta al JSON de Service Account de Firebase.
- INVITATION_JWT_SECRET: Llave secreta para JWT de invitaciones web.

**Comunicaciones (Twilio)**
- TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SERVICE_SID: Credenciales para validación OTP vía Meta/WhatsApp.

**Terceros**
- PERUDEVS_API_KEY: API Key para la consulta de RUC/DNI.
