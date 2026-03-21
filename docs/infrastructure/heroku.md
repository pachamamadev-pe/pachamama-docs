# Plataforma Heroku (MVP / Pre-Producción)

Los microservicios backend principales de la plataforma, basados en Java (Spring Boot), están orquestados y alojados en **Heroku**.

## Cuenta Principal

- **Propietario / Acceso de Administración:** `pachamamadev@gmail.com`

## Aplicaciones (Apps)

A continuación el mapeo entre nuestro repositorio de GitHub y el nombre de la App instanciada en Heroku:

| Repositorio de Código | Nombre de la App en Heroku |
|---|---|
| `pachamama-api-admin-java` | `pachamama-api-admin-java` |
| `pachamama-api-sync-java` | `pachamama-api-sync-java` |
| `pachamama-api-notifications-java` | `pachamama-api-notif-java` |
| `pachamama-api-trace-java` | `pachamama-api-trace-java` |

## Estrategia de Integración y Despliegue Continuo (CI/CD)

Todos los proyectos en Heroku son desplegados **automáticamente** utilizando **GitHub Actions**.

La regla general de nuestros workflows (`.github/workflows`) es:
1. Al realizar cambios (merges o commits) sobre la rama **`main`**, GitHub Actions dispara el workflow de despliegue.
2. El contenedor o empaquetado del repositorio correspondiente es constuido.
3. Se publica la nueva versión en la respectiva app bajo la cuenta de Heroku (`pachamamadev@gmail.com`), reiniciando los dynos automáticamente.
