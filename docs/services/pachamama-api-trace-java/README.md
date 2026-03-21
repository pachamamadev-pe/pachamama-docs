# Pachamama API Traceability (MVP / Pre-Producción)

Este microservicio provee la capa de lectura (Read-Model) enfocada en la trazabilidad de lotes y eventos para la Landing Page y tableros informativos. Está desarrollado en Java y desplegado en Heroku.

## Enlaces y Cuentas

- **Proveedor Cloud:** Heroku
- **Cuenta (Desarrollo/Propietario):** `pachamamadev@gmail.com`

## Stack Tecnológico

- **Lenguaje:** Java 21
- **Framework Base:** Quarkus `3.17.7`
- **Capa Exposición REST:** `quarkus-rest-jackson`
- **Capa Base de Datos:** MongoDB con Panache (`quarkus-mongodb-panache`)
- **Gestión de dependencias:** Maven

## Sistema de Control de Versiones

- **Repositorio:** `pachamama-api-trace-java`

## Despliegue e Infraestructura (CI/CD)

El despliegue de esta aplicación está completamente automatizado a través de workflows con **GitHub Actions**. Al realizarse un cambio sobre la rama `main`, se activa el pipeline que construye y despliega la nueva versión directamente en la app de Heroku.

Esta API expone consultas exclusivas de solo lectura (CQRS) sobre el seguimiento de recursos.
- Base de datos NoSQL: Consume lectura directamente desde la colección `pachamama_traceability_readmodel_dev` en MongoDB, la cual ha sido previamente populada de forma reactiva por la función Azure respectiva.
