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
