> Referencia del skill `pachamama-docs` — Estructura del Repositorio

# Estructura del Repositorio `pachamama-docs`

## Árbol de Directorios

```
pachamama-docs/
├── mkdocs.yml                         ← Navegación central (SIEMPRE actualizar al agregar archivos)
│
├── docs/
│   ├── index.md                       ← Página de inicio del sitio MkDocs
│   ├── ROADMAP-MIGRATION-PRD.md       ← Roadmap de migración a Azure
│   ├── MVP-ARCHITECTURE.md            ← Arquitectura MVP vigente
│   ├── roles-permisos.md              ← Reglas de negocio y permisos
│   │
│   ├── infrastructure/                ← Doc de cada proveedor cloud/DB
│   │   ├── azure.md
│   │   ├── heroku.md
│   │   ├── railway.md
│   │   ├── mongodb.md
│   │   ├── redis.md
│   │   ├── firebase.md
│   │   ├── vercel.md
│   │   └── twilio.md
│   │
│   ├── flujos/                        ← Flujos arquitectónicos con diagramas Mermaid
│   │   ├── sincronizacion-offline.md
│   │   ├── trazabilidad-cqrs.md
│   │   ├── gestion-archivos-sas.md
│   │   └── notificaciones-push.md
│   │
│   ├── services/                      ← README técnico de cada servicio
│   │   ├── pachamama-mobile-android/README.md
│   │   ├── pachamama-api-admin-java/README.md
│   │   ├── pachamama-api-sync-java/README.md
│   │   ├── pachamama-api-notifications-java/README.md
│   │   ├── pachamama-api-trace-java/README.md
│   │   ├── pachamama-func-sas-node/README.md
│   │   ├── pachamama-func-trace-sync/README.md
│   │   ├── pachamama-web-admin/README.md
│   │   └── pachamama-web-landing/README.md
│   │
│   ├── gestion-cambios/               ← ⭐ Registro de cambios funcionales
│   │   └── <slug-del-cambio>/
│   │       ├── index.md               ← Resumen integral (SIEMPRE existe)
│   │       └── <servicio>.md          ← Changelog detallado por servicio
│   │
│   └── referencias/                   ← Archivos de referencia y changelogs
│       ├── cambios-app.txt            ← Changelog cronológico master de la app móvil
│       └── cambios-en-implementacion/
│           └── <feature>/
│               └── changelog-<servicio>.md
│
└── arquitecturas/                     ← Documentos de arquitectura formal
    └── ARQ-<PROYECTO>-<PROVEEDOR>-<YYYYMMDD>[-v<N>].md
```

---

## Reglas por Sección

### `docs/gestion-cambios/`

| Regla | Detalle |
|-------|---------|
| Un cambio = una carpeta | Siempre crear subcarpeta con slug del cambio |
| `index.md` siempre | Resumen integral obligatorio en cada carpeta |
| `<servicio>.md` | Un archivo por cada servicio afectado en ese cambio |
| Orden en mkdocs.yml | Entradas más recientes **primero** (orden descendente) |

**Servicios en mkdocs.yml** (usar estos títulos exactos en la navegación):

| Archivo | Título en nav |
|---------|--------------|
| `index.md` | `Resumen Integral` |
| `pachamama-mobile-android.md` | `Mobile Android` |
| `pachamama-api-admin-java.md` | `API Admin` |
| `pachamama-api-sync-java.md` | `API Sync` |
| `pachamama-api-notifications-java.md` | `API Notificaciones` |
| `pachamama-api-trace-java.md` | `API Trazabilidad` |
| `pachamama-admin-web.md` | `Admin Web` |

> **Importante:** El frontend web admin se llama `pachamama-admin-web.md` en archivos (no `pachamama-web-admin.md`).

---

### `docs/infrastructure/`

- Un archivo `.md` por proveedor.
- Los proveedores existentes: `azure`, `heroku`, `railway`, `mongodb`, `redis`, `firebase`, `vercel`, `twilio`.
- Para agregar un nuevo proveedor: crear el archivo + añadir entrada en mkdocs.yml bajo "Infraestructura".

### `docs/flujos/`

- Un archivo `.md` por flujo técnico del sistema.
- Siempre incluir diagrama Mermaid.
- Para agregar un flujo nuevo: crear el archivo + añadir entrada en mkdocs.yml bajo "Flujos Arquitectónicos".

### `docs/services/`

- Un directorio por servicio, con `README.md` dentro.
- No requiere actualización de mkdocs.yml (los servicios ya están en la nav).

### `docs/referencias/`

- `cambios-app.txt`: changelog master del mobile. **Actualizar al inicio del archivo** cada vez que se documente un cambio que incluya `pachamama-mobile-android`.
- `cambios-en-implementacion/`: changelogs técnicos de bajo nivel generados durante el desarrollo.

### `arquitecturas/`

- Archivos de arquitectura formal, fuera del directorio `docs/`.
- No están bajo MkDocs, son documentos de referencia para el equipo técnico.

---

## Patrón en `mkdocs.yml`

### Agregar un cambio en Gestión de Cambios

```yaml
nav:
  - Gestión de Cambios:
    - "[DD-DD Mmm YYYY] Nombre del Nuevo Cambio":   # ← agregar aquí (primero)
      - Resumen Integral: gestion-cambios/<slug>/index.md
      - <Servicio 1>: gestion-cambios/<slug>/<servicio1>.md
      - <Servicio 2>: gestion-cambios/<slug>/<servicio2>.md
    - "[Entradas anteriores...]":                    # ← las existentes quedan debajo
```

### Agregar un flujo nuevo

```yaml
nav:
  - Flujos Arquitectónicos:
    - Nombre del Flujo: flujos/<slug>.md
    - (entradas existentes...)
```

### Agregar infraestructura nueva

```yaml
nav:
  - Infraestructura:
    - Nombre Proveedor: infrastructure/<proveedor>.md
    - (entradas existentes...)
```
