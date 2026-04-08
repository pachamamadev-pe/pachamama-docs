# Changelog — Pachamama API Notifications (Java)

**Cambio Relacionado:** Consentimiento Informado Cifrado y Gestión de Errores  
**Versión:** `v1.3.0`  
**Fecha:** 2026-04-08

---

## [v1.3.0] — 2026-04-08

### Added — Event Logging API

Nueva funcionalidad completa para registrar y consultar eventos de la aplicación en una colección dedicada de MongoDB (`events_logging`).

---

### Modelo — `EventLog`

Documento mapeado a la colección `events_logging` en MongoDB.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `String` | `_id` auto-generado por MongoDB |
| `traceId` | `String` *(indexado)* | Identificador de traza distribuida (UUID auto-generado si está ausente) |
| `channel` | `String` | Canal de origen: `app` o `web` |
| `channelVersion` | `String` | Versión del canal (ej. `android-2.3.1`) |
| `userId` | `String` *(indexado)* | Identificador del usuario |
| `tenantId` | `String` *(indexado)* | Identificador del tenant |
| `projectId` | `String` *(indexado)* | Identificador del proyecto |
| `onboardingId` | `String` *(indexado)* | Identificador del flujo de onboarding |
| `tag` | `String` *(indexado)* | Categoría del evento (ej. `LOGIN`, `PAYMENT`) |
| `process` | `String` | Nombre del proceso o flujo |
| `startTime` | `Long` | Tiempo de inicio del proceso en milisegundos |
| `endTime` | `Long` | Tiempo de fin del proceso en milisegundos |
| `durationMs` | `Long` | Duración calculada automáticamente (`endTime - startTime`) |
| `level` | `String` | Severidad del evento: `INFO`, `WARN`, `ERROR` |
| `message` | `String` | Mensaje descriptivo del evento |
| `errorMessage` | `String` | Mensaje de error (cuando aplique) |
| `errorStackTrace` | `String` | Stack trace completo (cuando aplique, no expuesto en responses) |
| `statusCode` | `String` | Código HTTP o de error de negocio |
| `clientIp` | `String` | IP del cliente |
| `userAgent` | `String` | Header User-Agent del cliente |
| `environment` | `String` | Entorno de despliegue: `local`, `dev`, `staging`, `prod` |
| `metadata` | `Map<String, Object>` | Datos extra en formato clave-valor |
| `createdAt` | `Instant` *(indexado)* | Timestamp auto-asignado en creación |

---

### Endpoint — `POST /api/events-logging`

Registra un nuevo evento. Devuelve `201 Created`.

**Request body (`EventLogRequest`):**
- `channel` — requerido, debe ser `app` o `web`
- `tag` — requerido
- `level` — requerido, debe ser `INFO`, `WARN` o `ERROR`
- Resto de campos opcionales.

**Ejemplo cURL:**
```bash
curl -X POST http://localhost:8082/api/events-logging \
  -H "Content-Type: application/json" \
  -d '{
    "traceId": "trace-abc-123",
    "channel": "app",
    "channelVersion": "android-3.1.0",
    "userId": "user-001",
    "tenantId": "tenant-xyz",
    "projectId": "proj-001",
    "onboardingId": "onboard-001",
    "tag": "LOGIN",
    "process": "auth-flow",
    "startTime": 1712500000000,
    "endTime": 1712500001500,
    "level": "INFO",
    "message": "User logged in successfully",
    "statusCode": "200",
    "environment": "prod",
    "metadata": { "deviceId": "device-999", "appVersion": "3.1.0" }
  }'
```

---

### Endpoints de Consulta — `GET /api/events-logging/...`

Todos los endpoints paginados soportan `?page=0&size=20`.

| Método | Path | Descripción |
|---|---|---|
| `GET` | `/api/events-logging/{id}` | Obtener evento por ID (`404` si no existe) |
| `GET` | `/api/events-logging/user/{userId}` | Listar por usuario |
| `GET` | `/api/events-logging/tag/{tag}` | Listar por tag |
| `GET` | `/api/events-logging/process/{process}` | Listar por proceso |
| `GET` | `/api/events-logging/level/{level}` | Listar por nivel (`INFO`/`WARN`/`ERROR`) |
| `GET` | `/api/events-logging/channel/{channel}` | Listar por canal (`app`/`web`) |
| `GET` | `/api/events-logging/trace/{traceId}` | Listar por traceId |
| `GET` | `/api/events-logging/tenant/{tenantId}` | Listar por tenant |
| `GET` | `/api/events-logging/project/{projectId}` | Listar por proyecto |
| `GET` | `/api/events-logging/onboarding/{onboardingId}` | Listar por onboarding |
| `GET` | `/api/events-logging/range` | Listar por rango de fechas (`from` / `to` ISO-8601) |
| `GET` | `/api/events-logging/user/{userId}/tag/{tag}` | Listar por usuario + tag |
| `GET` | `/api/events-logging/level/{level}/process/{process}` | Listar por nivel + proceso |

---

### Clases Nuevas

| Clase | Descripción |
|---|---|
| `model/EventLog.java` | Documento MongoDB mapeado a `events_logging` |
| `dto/EventLogRequest.java` | Record de entrada para registro de eventos (con validaciones) |
| `dto/EventLogResponse.java` | Record de respuesta (todos los campos excepto `errorStackTrace`) |
| `repository/EventLogRepository.java` | Extiende `MongoRepository`, incluye métodos de consulta por todos los campos indexados |
| `service/EventLogService.java` | Lógica de negocio: registro, auto-UUID de traceId, cálculo de `durationMs`, consultas paginadas |
| `controller/EventLogController.java` | Controlador REST en `/api/events-logging` con documentación Swagger |

---

## Historial de Versiones Previas

| Versión | Fecha | Resumen |
|---|---|---|
| `v1.2.0` | 2026-02-14 | `NotificationQueryController`, `AzureServiceBusSubscriber`, correcciones Service Bus y MongoDB SSL |
| `v1.1.0` | 2026-02-01 | Integración FCM, `NotificationController`, `NotificationLog` en MongoDB |
| `v1.0.0` | 2026-01-15 | Scaffolding inicial, Dockerfile, configuración Heroku y Azure Service Bus |
