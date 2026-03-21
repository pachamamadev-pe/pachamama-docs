# Pachamama API Admin (MVP / Pre-Producción)

Este es el backend principal de la plataforma, encargado de la gestión operativa (comunidades, recolectores, brigadas, proyectos, etc.). Está desarrollado en Java (Spring Boot) y se encuentra alojado en Heroku. Esta configuración corresponde al entorno de pre-producción (MVP).

## Características del Servicio

### Stack Tecnológico

- **Lenguaje:** Java 21
- **Framework Base:** Spring Boot 3.3.1
- **Compilación/Gestión de dependencias:** Maven
- **Arquitectura:** Monolito / Multi-módulo (pp, common, security, persistence, módulos por dominio como rigades, collectors, etc.)

## Integraciones del Servicio

Este servicio principal actúa como orquestador y se integra a nivel de negocio y técnico con:
- **Base de Datos (Railway):** Persistencia operativa leyendo/escribiendo hacia la base principal PostgreSQL (+ PostGIS).
- **Caché (Indefinido/Heroku Addon):** Utiliza Redis para cacheo de respuestas (DBR).
- **Autenticación (Firebase):** Validación de los tokens emitidos hacia el cliente móvil o web.
- **Mensajería Interna (Azure Service Bus):** Publica eventos/mensajes asíncronos en los tópicos (ssigned-brigade y 	raceability-events-dev).
- **Proveedores Externos:**
  - **Twilio**: Servicio de Send/Verify OTP para autenticación.
  - **API Perú Devs**: Consultas externas de tipo DNI/RUC.
  - **Azure Storage:** Carga e indexación de archivos al Blob (dmin-uploads).

## Despliegue / Repositorio

- **Repositorio:** pachamama-api-admin-java
- **Alojamiento:** Heroku (App: pachamama-api-admin-java)
- **CI/CD:** Completamente automatizado usando **GitHub Actions**. Compila y despliega en cada push/merge a la rama main hacia el Dyno usando los credenciales en secret de la cuenta dueña.
