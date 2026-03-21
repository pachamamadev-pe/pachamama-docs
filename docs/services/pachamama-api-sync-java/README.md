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
