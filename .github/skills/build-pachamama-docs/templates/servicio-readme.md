> Plantilla del skill `pachamama-docs` — README de Servicio

---

```markdown
# [NOMBRE_LEGIBLE_DEL_SERVICIO] ([AMBIENTE: MVP / Pre-Producción / Producción])

[Párrafo de descripción: Rol del servicio en la arquitectura Pachamama, qué hace y con quién interactúa.]

---

## Características del Servicio

### Stack Tecnológico

| Elemento | Tecnología |
|----------|-----------|
| Plataforma de hosting | [Heroku / Azure App Service / Azure Functions / Vercel / Railway] |
| Lenguaje | [Java 17+ / Kotlin / TypeScript / Node.js] |
| Framework | [Spring Boot 3.x / React / Next.js] |
| Arquitectura | [REST API / SPA / Serverless / Offline-first MVVM] |
| Base de datos (si aplica) | [PostgreSQL 16 + PostGIS / Cosmos DB / Room DB / Redis] |

### Dependencias Externas

| Servicio externo | Integración |
|-----------------|-------------|
| [NOMBRE_SERVICIO_EXTERNO] | [Descripción del uso] |

---

## Integraciones del Servicio

```
[NOMBRE_SERVICIO]
  ├─→ [SERVICIO_1]     ← [Descripción breve de la integración]
  ├─→ [SERVICIO_2]     ← [Descripción breve de la integración]
  └─→ [SERVICIO_3]     ← [Descripción breve de la integración]
```

---

## Distribución / Repositorio

| Campo | Valor |
|-------|-------|
| Repositorio GitHub | `[nombre-del-repositorio]` |
| Branch principal | `main` |
| CI/CD | [GitHub Actions / Heroku Auto-deploy / Manual] |
| Método de despliegue | [Heroku Git Push / Docker / ZIP deploy] |
| URL producción | `https://[url.del.servicio]` |

---

## Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/[recurso]` | [Descripción] |
| POST | `/api/v1/[recurso]` | [Descripción] |

<!-- Solo para APIs. Omitir esta sección para apps móviles, frontends y functions. -->

---

## Variables de Entorno Requeridas

| Variable | Descripción |
|----------|-------------|
| `[VARIABLE_1]` | [Para qué se usa] |
| `[VARIABLE_2]` | [Para qué se usa] |

---

## Versión Actual

| Ambiente | Versión | Fecha |
|----------|---------|-------|
| Producción | `v[X.Y.Z]` | [Mes YYYY] |

<!-- Omitir si el versioning no aplica (functions, landing) -->
```

---

## Secciones Obligatorias

| Sección | Aplica a |
|---------|---------|
| `# Nombre (Ambiente)` | Todos |
| Párrafo introductorio | Todos |
| Stack Tecnológico | Todos |
| Distribución / Repositorio | Todos |

## Secciones Opcionales (por tipo)

| Sección | Solo para |
|---------|-----------|
| Endpoints Principales | APIs REST (api-admin, api-sync, api-notifications, api-trace) |
| Variables de Entorno Requeridas | APIs y Functions |
| Integraciones del Servicio | Servicios con múltiples dependencias |
| Versión Actual | Mobile Android, APIs |

---

## Ejemplo — `pachamama-api-sync-java`

```markdown
# Pachamama API Sync Java (Pre-Producción)

API REST encargada de procesar la sincronización de datos recolectados offline
por la app Android. Consume mensajes de Azure Service Bus y persiste las 
actividades forestales en PostgreSQL + PostGIS (Railway).

---

## Características del Servicio

### Stack Tecnológico

| Elemento | Tecnología |
|----------|-----------|
| Plataforma de hosting | Heroku (migración → Azure App Service Jul 2026) |
| Lenguaje | Java 17 |
| Framework | Spring Boot 3.2 |
| Arquitectura | REST API + Service Bus Consumer |
| Base de datos | PostgreSQL 16 + PostGIS (Railway) |

---

## Integraciones del Servicio

```
pachamama-api-sync-java
  ├─→ Azure Service Bus     ← Consume cola de mensajes de sincronización
  ├─→ PostgreSQL + PostGIS  ← Persiste actividades y coordenadas GPS
  └─→ pachamama-api-trace   ← Publica eventos CQRS al topic de trazabilidad
```

---

## Distribución / Repositorio

| Campo | Valor |
|-------|-------|
| Repositorio GitHub | `pachamama-api-sync-java` |
| Branch principal | `main` |
| CI/CD | GitHub Actions → Heroku |
| URL producción | `https://pachamama-api-sync.herokuapp.com` |
```
