# Pachamama API Sync (MVP / Pre-Producción)

Este microservicio se encarga de gestionar la sincronización asíncrona (offline-first) desde los dispositivos móviles (App). Está desarrollado en Java y desplegado en Heroku.

## Enlaces y Cuentas

- **Proveedor Cloud:** Heroku
- **Cuenta (Desarrollo/Propietario):** `pachamamadev@gmail.com`

## Stack Tecnológico

- **Lenguaje:** Java 21 
- **Framework Base:** Spring Boot `3.5.10-SNAPSHOT`
- **Mensajería:** Spring Cloud Azure `6.1.0` (para Azure Service Bus)
- **Gestión de dependencias:** Maven
- **Arquitectura:** Arquitectura Hexagonal / Puertos y Adaptadores (`adapter`, `application`, `domain`)

## Sistema de Control de Versiones

- **Repositorio:** `pachamama-api-sync-java`

## Despliegue e Infraestructura (CI/CD)

El despliegue de esta aplicación está completamente automatizado a través de workflows con **GitHub Actions**. Al realizarse un cambio sobre la rama `main`, se activa el pipeline que construye y despliega la nueva versión directamente en la app de Heroku.

El servicio expone endpoints REST consumidos por la App Móvil para encolar actividades en modo offline.
Internamente, la API interactúa con:
- Colas de mensajería (Service Bus en Azure - `activities-sync-queue`).
- Persistencia asíncrona hacia la base de datos principal PostgreSQL.
