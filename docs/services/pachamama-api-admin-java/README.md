# Pachamama API Admin (MVP / Pre-Producción)

Este es el backend principal de la plataforma, encargado de la gestión operativa (comunidades, recolectores, brigadas, proyectos, etc.). Está desarrollado en Java (Spring Boot) y se encuentra alojado en Heroku. Esta configuración corresponde al entorno de pre-producción (MVP).

## Enlaces y Cuentas

- **Proveedor Cloud:** Heroku
- **Cuenta (Desarrollo/Propietario):** `pachamamadev@gmail.com`

## Stack Tecnológico

- **Lenguaje:** Java 21
- **Framework Base:** Spring Boot `3.3.1`
- **Compilación/Gestión de dependencias:** Maven
- **Arquitectura:** Monolito / Multi-módulo (`app`, `common`, `security`, `persistence`, módulos por dominio como `brigades`, `collectors`, etc.)

## Sistema de Control de Versiones

- **Repositorio:** `pachamama-api-admin-java`

## Despliegue (CI/CD)

El despliegue de esta aplicación está completamente automatizado a través de workflows con **GitHub Actions**. Al realizarse un cambio sobre la rama `main`, se activa el pipeline que construye y despliega la nueva versión directamente en la app de Heroku.

La aplicación utiliza la infraestructura de contenedores / buildpacks de Heroku.
Internamente, la API se conecta a:
- Base de datos relacional (PostgreSQL en Railway).
- Caché (Redis).
- Servicios de autenticación y mensajería (Firebase, Twilio, etc.).

*(Esta sección se ampliará conforme se documenten las variables de entorno y los add-ons específicos instalados en Heroku).*
