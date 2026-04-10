> Referencia del skill `pachamama-docs` — Catálogo de Servicios del Sistema

# Servicios del Sistema Pachamama

## Tabla Maestra

| Clave de servicio | Archivo en `gestion-cambios/` | Título nav mkdocs | Descripción |
|-------------------|------------------------------|-------------------|-------------|
| `pachamama-mobile-android` | `pachamama-mobile-android.md` | Mobile Android | App Android para recolectores de campo (offline-first, Kotlin) |
| `pachamama-api-admin-java` | `pachamama-api-admin-java.md` | API Admin | API REST Java Spring Boot — configuraciones, onboarding, KPIs, gestión de brigadas |
| `pachamama-api-sync-java` | `pachamama-api-sync-java.md` | API Sync | API REST Java Spring Boot — sincronización offline → PostgreSQL + PostGIS |
| `pachamama-api-notifications-java` | `pachamama-api-notifications-java.md` | API Notificaciones | API REST Java Spring Boot — FCM push notifications, Twilio OTP WhatsApp |
| `pachamama-api-trace-java` | `pachamama-api-trace-java.md` | API Trazabilidad | API REST Java Spring Boot — ReadModel CQRS, Cosmos DB |
| `pachamama-func-sas-node` | *(no usualmente en gestion-cambios)* | — | Azure Function Node.js — generación de SAS tokens para Blob Storage |
| `pachamama-func-trace-sync` | *(no usualmente en gestion-cambios)* | — | Azure Function — Trace Sync (Service Bus → Cosmos DB) |
| `pachamama-web-admin` | `pachamama-admin-web.md` | Admin Web | Frontend React + TypeScript — Panel de administración |
| `pachamama-web-landing` | *(no usualmente en gestion-cambios)* | — | Web Landing (marketing) — React o Next.js |

> **Nota de nombre de archivo crítica:**  
> El servicio `pachamama-web-admin` se documenta en `pachamama-admin-web.md` dentro de `gestion-cambios/`,  
> **no** `pachamama-web-admin.md`. Este es el único servicio con nombre de archivo diferente a su clave.

---

## Detalles por Servicio

### `pachamama-mobile-android`

```
Tipo:        Aplicación móvil nativa Android
Lenguaje:    Kotlin
Arquitectura: MVVM + Clean Architecture
Características:
  - Offline-first (Room + WorkManager)
  - Sincronización con pachamama-api-sync-java via Azure Service Bus
  - Auth via Firebase Auth
  - Notificaciones push via FCM (pachamama-api-notifications-java)
  - SAS tokens para uploads a Azure Blob Storage
  - OTP via Twilio WhatsApp
Versionado: Semantic versioning vMAJOR.MINOR.PATCH
Repositorio: pachamama-mobile-android (GitHub)
```

### `pachamama-api-admin-java`

```
Tipo:        API REST backend
Lenguaje:    Java 17+
Framework:   Spring Boot 3.x
Hosting:     Heroku (migración a Azure App Service en 2026)
Responsabilidades:
  - CRUD de brigadistas y cuadrillas
  - Configuración de formularios / KPIs
  - Reportes y exportación de datos
  - Gestión de permisos y roles
Base de datos: PostgreSQL 16 + PostGIS (Railway)
```

### `pachamama-api-sync-java`

```
Tipo:        API REST backend
Lenguaje:    Java 17+
Framework:   Spring Boot 3.x
Hosting:     Heroku (migración a Azure App Service en 2026)
Responsabilidades:
  - Recibir y procesar mensajes de sincronización desde Azure Service Bus
  - Insertar/actualizar registros de campo en PostgreSQL + PostGIS
  - Gestionar conflictos de sincronización offline
Base de datos: PostgreSQL 16 + PostGIS (Railway)
```

### `pachamama-api-notifications-java`

```
Tipo:        API REST backend
Lenguaje:    Java 17+
Framework:   Spring Boot 3.x
Hosting:     Heroku (migración a Azure App Service en 2026)
Responsabilidades:
  - Enviar notificaciones push via Firebase Cloud Messaging (FCM)
  - Enviar OTP y mensajes via Twilio WhatsApp
Integraciones: Firebase Admin SDK, Twilio SDK
```

### `pachamama-api-trace-java`

```
Tipo:        API REST backend (ReadModel / CQRS)
Lenguaje:    Java 17+
Framework:   Spring Boot 3.x
Hosting:     Heroku (migración a Azure App Service en 2026)
Responsabilidades:
  - Proveer ReadModel de trazabilidad para el Admin Web
  - Consultar Cosmos DB (colección de eventos)
Base de datos: Azure Cosmos DB (MongoDB API)
```

### `pachamama-func-sas-node`

```
Tipo:        Serverless Function
Lenguaje:    Node.js / TypeScript
Hosting:     Azure Functions (ya en Azure desde MVP)
Responsabilidades:
  - Generar SAS tokens efímeros para uploads directos del mobile a Azure Blob Storage
  - Token válido por tiempo limitado por archivo/operación
```

### `pachamama-func-trace-sync`

```
Tipo:        Serverless Function (Azure Function trigger: Service Bus)
Lenguaje:    Node.js o Java
Hosting:     Azure Functions
Responsabilidades:
  - Consumir mensajes de trazabilidad desde Azure Service Bus Topic
  - Persistir eventos en Azure Cosmos DB
```

### `pachamama-web-admin`

```
Tipo:        Frontend web SPA
Lenguaje:    TypeScript
Framework:   React
Hosting:     Vercel (gratuito; migración a Azure Static Web Apps en 2026)
Responsabilidades:
  - Panel de administración para supervisores y coordinadores
  - Visualización de KPIs, mapas con datos PostGIS, reportes
  - Consumidora de pachamama-api-admin-java y pachamama-api-trace-java
```

### `pachamama-web-landing`

```
Tipo:        Frontend web (sitio de marketing)
Framework:   React o Next.js
Hosting:     Vercel (gratuito)
```

---

## Integraciones entre Servicios

```
pachamama-mobile-android
  ├─→ pachamama-api-sync-java          (sincronización de actividades)
  ├─→ pachamama-api-notifications-java (FCM push, OTP)
  ├─→ pachamama-func-sas-node          (SAS token para fotos/adjuntos)
  └─→ Firebase Auth                    (autenticación)

pachamama-api-sync-java
  └─→ Azure Service Bus                (cola de mensajes desde el mobile)

pachamama-func-trace-sync
  ├─→ Azure Service Bus                (consume topic de trazabilidad)
  └─→ Azure Cosmos DB                  (escribe eventos)

pachamama-api-trace-java
  └─→ Azure Cosmos DB                  (lee eventos para ReadModel)

pachamama-web-admin
  ├─→ pachamama-api-admin-java         (gestión y configuración)
  └─→ pachamama-api-trace-java         (trazabilidad y KPIs)
```

---

## Servicios Externos Permanentes (no se migran)

| Servicio | Proveedor | Rol |
|----------|-----------|-----|
| Firebase Auth | Google | Autenticación de usuarios |
| Firebase Cloud Messaging | Google | Push notifications al mobile |
| Twilio WhatsApp | Twilio | OTP y notificaciones vía WhatsApp |
