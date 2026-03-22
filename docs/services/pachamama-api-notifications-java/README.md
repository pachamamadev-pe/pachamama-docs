# Pachamama API Notificaciones (MVP / Pre-Producción)

Este microservicio se especializa en el envío de notificaciones y alertas hacia los usuarios. Desarrollado en Java y operando desde Heroku.

## Características del Servicio

### Stack Tecnológico

- **Lenguaje:** Java 21
- **Framework Base:** Spring Boot 3.4.2
- **Mensajería:** azure-messaging-servicebus 7.17.6 (para colas/tópicos de Azure)
- **Persistencia:** Spring Boot Starter Data MongoDB
- **Proveedores de Notificación:** firebase-admin 9.3.0
- **Gestión de dependencias:** Maven

## Integraciones del Servicio

Este servicio se suscribe a los eventos lógicos del negocio para emitir notificaciones omnicanal. Sus integraciones son:
- **Tópicos Azure (Service Bus):** Es consumidor (sub:send-notifications) desde tópico assigned-brigade para reaccionar a una asignación y notificar al usuario final.
- **Base de datos (MongoDB Atlas):** Persistencia y auditoría de eventos de notificación (pachamama_notifications).
- **Mensajería Push (Firebase):** Integración nativa (APP -- REST --> API3) y comunicación REST hacia Firebase Cloud Messaging (FCM) para enviar Push Notifications a los recolectores de la Mobile App.

## Despliegue / Repositorio

- **Repositorio:** pachamama-api-notifications-java
- **Alojamiento:** Heroku (App: pachamama-api-notif-java)
- **CI/CD:** El despliegue de esta aplicación está completamente automatizado a través de workflows con **GitHub Actions**. Al realizarse un cambio sobre la rama main, se activa el pipeline.

## Configuración y Variables de Entorno

Para levantar este microservicio de envío de notificaciones mediante eventos u orquestación, es necesario configurar:

**General**
- SPRING_PROFILES_ACTIVE: Perfil activo (ej. local, dev).
- PORT o SERVER_PORT: Puerto expuesto por el aplicativo.

**Base de Datos (MongoDB Atlas)**
- MONGODB_URI: Cadena de conexión de Mongo (incluye auth y cluster).
- MONGODB_DATABASE: Nombre de la DB (ej. pachamama_notifications).

**Mensajería Push (Firebase Cloud Messaging)**
- FIREBASE_PROJECT_ID: ID del proyecto (ej. pachamama-mvp).
- FIREBASE_CREDENTIALS_JSON_FILE: Archivo JSON de Service Account (o cargado mediante variables base en Base64).
- FIREBASE_CLIENT_EMAIL: Email del service account.
- FIREBASE_PRIVATE_KEY: Llave privada RSA.

**Azure Service Bus (Suscripción a Tópicos)**
- AZURE_SERVICEBUS_ENABLED: Habilitación de la escucha (listeners).
- AZURE_SERVICEBUS_CONNECTION_STRING: Cadena de conexión al SB.
- AZURE_SERVICEBUS_TOPIC_NAME: Nombre del tópico a escuchar (ej. ssigned-brigade).
- AZURE_SERVICEBUS_SUBSCRIPTION_NAME: Nombre de la suscripción (ej. send-notifications).
