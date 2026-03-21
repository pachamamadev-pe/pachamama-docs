# Pachamama API Notificaciones (MVP / Pre-Producción)

Este microservicio se especializa en el envío de notificaciones y alertas hacia los usuarios. Desarrollado en Java y operando desde Heroku.

## Enlaces y Cuentas

- **Proveedor Cloud:** Heroku
- **Cuenta (Desarrollo/Propietario):** `pachamamadev@gmail.com`

## Stack Tecnológico

- **Lenguaje:** Java 21
- **Framework Base:** Spring Boot `3.4.2`
- **Mensajería:** `azure-messaging-servicebus` `7.17.6` (para colas/tópicos de Azure)
- **Persistencia:** Spring Boot Starter Data MongoDB
- **Proveedores de Notificación:** `firebase-admin` `9.3.0`
- **Gestión de dependencias:** Maven

## Sistema de Control de Versiones

- **Repositorio:** `pachamama-api-notifications-java`
- **Nombre en Heroku:** `pachamama-api-notif-java`

## Despliegue e Infraestructura (CI/CD)

El despliegue de esta aplicación está completamente automatizado a través de workflows con **GitHub Actions**. Al realizarse un cambio sobre la rama `main`, se activa el pipeline que construye y despliega la nueva versión directamente en la app de Heroku (`pachamama-api-notif-java`).

El servicio se suscribe a los eventos (ej. un recolector o brigada fue asignada) para emitir las notificaciones pertinentes.
Consumos y dependencias:
- Base de datos NoSQL: MongoDB (`pachamama_notifications`).
- Pub/Sub: Consume tópicos desde Azure Service Bus (ej. `assigned-brigade`).
- Mensajería externa: Firebase Cloud Messaging (FCM) para push notifications nativas.
