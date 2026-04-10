> Referencia del skill `pachamama-docs` — Contexto del Sistema Pachamama

# Contexto del Sistema Pachamama

## ¿Qué es Pachamama?

Pachamama es una plataforma de **recolección de datos en campo** orientada a brigadistas forestales y supervisores en Perú / LATAM.  
Desarrollada por **REORI CORP S.A.C.** bajo la dirección de **Jecri Do Santos**.

---

## Flujo Principal del Sistema

```
[Brigadista en campo]
        │
        ▼ (offline primero, sincroniza al recuperar señal)
[App Android — pachamama-mobile-android]
        │
        ▼ (mensajes de sincronización vía Azure Service Bus)
[API Sync — pachamama-api-sync-java]
        │
        ▼ escribe
[PostgreSQL 16 + PostGIS — Railway → Azure Flexible Server]
        │
        ├─ datos operativos →  [API Admin — pachamama-api-admin-java]
        │                               │
        │                               ▼ consume
        │                      [Admin Web — pachamama-web-admin]
        │
        └─ eventos CQRS → [Azure Service Bus Topic]
                                   │
                                   ▼ (Function trigger)
                          [pachamama-func-trace-sync]
                                   │
                                   ▼ escribe
                          [Azure Cosmos DB — colección de eventos]
                                   │
                                   ▼ consume
                          [API Trace — pachamama-api-trace-java]
                                   │
                                   ▼ ReadModel
                          [Admin Web — trazabilidad y KPIs]

[Archivos/fotos en campo]
        │
        ▼ solicita SAS token
[pachamama-func-sas-node]
        │
        ▼ upload directo
[Azure Blob Storage]

[Notificaciones / OTP]
[pachamama-api-notifications-java]
  ├─→ Firebase Cloud Messaging  (push al mobile)
  └─→ Twilio WhatsApp           (OTP de verificación)
```

---

## Stack Tecnológico Actual (Pre-Migración, ~$87–103/mes)

| Componente | Proveedor / Tecnología | Costo mensual aprox. |
|-----------|------------------------|---------------------|
| 4 APIs Java (admin, sync, notifications, trace) | Heroku (dyno) | ~$80 USD |
| PostgreSQL 16 + PostGIS | Railway | ~$5 USD |
| Admin Web + Landing Web | Vercel | Gratuito |
| MongoDB Atlas (Cosmos DB API) | MongoDB Atlas M0 | Gratuito |
| Redis v8.2 | Redis Labs / Upstash | Gratuito / variable |
| Azure Functions + Storage + Service Bus | Azure Personal | ~$2 USD |
| Firebase Auth + FCM | Google Firebase | Gratuito (plan Spark) |
| Twilio WhatsApp OTP | Twilio | Variable (pay-as-you-go) |

---

## Plan de Migración Azure (Junio–Agosto 2026)

**Objetivo:** Migrar todo el stack a **Azure Corporativo** (`pachamamadev@pachamaxter.onmicrosoft.com`, región `brazilsouth`).  
**Costo objetivo:** ~$334.94 USD/mes en producción.

### Timing de Migración (3 olas)

| Ola | Mes | Servicios |
|-----|-----|-----------|
| Ola 1 | Junio 2026 | Functions + Storage + Service Bus (ya en Azure, actualizar a corporativo) |
| Ola 2 | Julio 2026 | APIs Java → Azure App Service; PostgreSQL → Azure Flexible Server |
| Ola 3 | Agosto 2026 | MongoDB → Cosmos DB for MongoDB; Redis → Azure Cache for Redis; Web → Azure Static Web Apps |

### Servicios que NO se migran (permanentes)

- Firebase Auth (mantiene sesiones del mobile)
- Firebase Cloud Messaging (FCM push notifications)
- Twilio WhatsApp OTP

### Referencia del documento de arquitectura

```
arquitecturas/ARQ-PACHAMAMA-AZURE-FULL-20260410-v2.md
```

---

## Características Clave del Producto

| Característica | Descripción |
|----------------|-------------|
| Offline-first | La app Android funciona sin conexión; sincroniza cuando hay señal |
| Geo-espacial | Los datos de campo incluyen coordenadas GPS con PostGIS |
| Trazabilidad CQRS | Patrón CQRS para auditoría completa de actividades forestales |
| Multi-brigada | Soporte para múltiples brigadas, cuadrillas y supervisores |
| Consentimiento informado | Proceso de firma digital con cifrado (feature en producción) |
| Notificaciones en tiempo real | FCM push + OTP WhatsApp para verificación de campo |

---

## Historial de Cambios Documentados

| Versión APK | Período | Cambio | Carpeta |
|-------------|---------|--------|---------|
| v1.2.1 | 8-9 Abr 2026 | Permisos Requeridos (Android) | `permisos-requeridos/` |
| v1.2.0 | — | Trazabilidad de versión de app | `trazabilidad-app-version/` |
| v1.1.0 | — | Observación KPI Sincronización | `observacion-kpi-sincronizacion/` |
| v1.0.0 | — | Consentimiento Informado Cifrado | `consentimiento-informado-cifrado/` |

---

## Roles Principales del Sistema

| Rol | Descripción |
|-----|-------------|
| Brigadista | Usa la app Android en campo para registrar actividades forestales |
| Supervisor | Gestiona su brigada vía Admin Web, revisa KPIs |
| Coordinador | Acceso administrativo completo, configura formularios y brigadas |
| Admin del sistema | Gestión técnica de la plataforma (REORI CORP) |

---

## Entornos / Ambientes

| Ambiente | Estado | Descripción |
|----------|--------|-------------|
| Desarrollo | Activo | Configuración local + servicios compartidos |
| Producción | Activo | Stack Heroku + Railway + Azure Personal |
| Azure Corporativo | Planificado (Jun 2026) | Migración completa `brazilsouth` |
