# Documentación de Pachamama

Bienvenido a la documentación oficial del ecosistema de Pachamama.

En este portal agrupamos toda la información arquitectónica, técnica y de operaciones de los distintos ambientes del proyecto.

## Índices de Arquitectura

- [Arquitectura MVP (Pre-Producción)](./MVP-ARCHITECTURE.md)

## Infraestructura y Cloud
- [Cuentas y Plataforma Heroku](./infrastructure/heroku.md)
- [Cuentas y Plataforma Vercel](./infrastructure/vercel.md)
- [Plataforma Azure](./infrastructure/azure.md)
- [Base de Datos Relacional: Railway (PostgreSQL)](./infrastructure/railway.md)
- [Base de Datos NoSQL: MongoDB Atlas](./infrastructure/mongodb.md)
- [Caché: Redis](./infrastructure/redis.md)
- [Identidad y Móvil: Firebase](./infrastructure/firebase.md)
- [Proveedor de Comunicaciones: Twilio & Meta](./infrastructure/twilio.md)

## Reglas de Negocio y Seguridad
- [Roles y Permisos del Sistema (MVP)](./roles-permisos.md)

## Catálogo de Servicios (MVP / Pre-Producción)

### Frontend
- [Pachamama Web Landing Page](./services/pachamama-web-landing/README.md)
- [Pachamama Web Admin](./services/pachamama-web-admin/README.md)
- [Pachamama Mobile App (Android)](./services/pachamama-mobile-android/README.md)

### Backend (Java en Heroku)
- [API Admin (Java)](./services/pachamama-api-admin-java/README.md)
- [API Notificaciones (Java)](./services/pachamama-api-notifications-java/README.md)
- [API Sync (Java)](./services/pachamama-api-sync-java/README.md)
- [API Traceability (Java)](./services/pachamama-api-trace-java/README.md)

### Tareas Asíncronas (Azure Functions)
- [Func: SAS Token Generator](./services/pachamama-func-sas-node/README.md)
- [Func: Traceability Sync](./services/pachamama-func-trace-sync/README.md)
