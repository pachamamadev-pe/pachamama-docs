# Plataforma Firebase (MVP / Pre-Producción)

**Firebase** provee servicios de identidad y Cloud nativos que son principalmente explotados por parte de la aplicación móvil y protección de APIS.

## Cuentas

- **Cuenta Principal:** `[Pendiente de definir]`
- **Consola:** Google IAM / Proyecto Firebase Pachamama Dev.

## Integraciones y Configuraciones Cloud

### Módulos Integrados (Servicios)

- **Firebase Authentication (Auth / FAUTH):**
    - Proveedor de identidades y generador de tokens JWT. 
    - Las web apps solicitan el login aquí. Una vez recibido el token, el Backend (`pachamama-api-admin-java`) lo interroga de forma severa contra Firebase para validarlo bajo cada request segurizado (Middleware).
- **Firebase Cloud Messaging (MESS):**
    - Infraestructura de entrega de notificaciones (Push).
    - Es llamado vía protocolo REST por el `pachamama-api-notifications-java` con la finalidad técnica de enviar notificaciones al `pachamama-mobile-android`.