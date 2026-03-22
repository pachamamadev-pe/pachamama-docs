# Plataforma Heroku (MVP / Pre-Producción)

Los microservicios backend principales de la plataforma, basados en Java (Spring Boot), están orquestados y alojados en **Heroku**.

## Cuentas

- **Cuenta Principal:** pachamamadev@gmail.com
- **Uso:** Alojamiento de los microservicios Java y gestión de los Dynos para el entorno MVP.

## Integraciones y Configuraciones Cloud

### Mapeo de Aplicaciones (Apps)

A continuación el mapeo entre nuestro repositorio de GitHub y el nombre de la App instanciada en Heroku:

| Repositorio de Código | Nombre de la App en Heroku |
|---|---|
| pachamama-api-admin-java | pachamama-api-admin-java |
| pachamama-api-sync-java | pachamama-api-sync-java |
| pachamama-api-notifications-java | pachamama-api-notif-java |
| pachamama-api-trace-java | pachamama-api-trace-java |

### Configuración CI/CD (GitHub Actions)

La integración continua y el despliegue hacia Heroku están **completamente automatizados** a través de **GitHub Actions**.

**Variables/Secrets requeridos en GitHub para Heroku:**
- HEROKU_API_KEY: Token de autorización de la cuenta pachamamadev@gmail.com.
- HEROKU_APP_NAME: *(Opcional, en base al workflow)* Nombre del aplicativo destino.
- HEROKU_EMAIL: Correo del propietario de la cuenta.

**Flujo de despliegue:**
1. Al realizar cambios sobre la rama **main**, se dispara el workflow (deploy-heroku.yml).
2. Se construye el compilado utilizando Maven.
3. Se despliega mediante el método estándar de buildpacks de Heroku, ejecutando el reinicio del Dyno automáticamente.
