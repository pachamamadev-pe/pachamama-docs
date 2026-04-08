# Changelog — Pachamama Mobile Android

**Versiones:** `v1.1.0` → `v1.2.0`  
**Cambio Relacionado:** Consentimiento Informado Cifrado y Gestión de Errores en Sincronización  
**Período:** 30 de Marzo – 8 de Abril 2026

---

## [v1.2.0] — 2026-04-08

### Novedades — Consentimiento informado personalizado y cifrado

#### Nuevo endpoint de consentimiento cifrado
- Se integró el endpoint `POST /api/v1/collectors/onboarding/legal-documents/encrypted`
  como mecanismo principal para obtener el consentimiento informado durante el onboarding.
- El documento devuelto contiene los parámetros `[[...]]` reemplazados por el backend
  con información real del recolector y de la empresa cliente asociada al token de invitación:
  `[[NOMBRE_RECOLECTOR]]`, `[[DNI_RECOLECTOR]]`, `[[RAZON_SOCIAL_CLIENTE]]`,
  `[[RUC_CLIENTE]]`, `[[DIRECCION_CLIENTE]]`, `[[VERSION]]`, etc.
- Mecanismo de cifrado: **RSA-OAEP + AES-256-GCM** con la misma clave pública cacheada
  que se usa en `submitOnboardingEncrypted`.

#### Modelo — `LegalDocumentRequest`
- Añadido `data class LegalDocumentRequest` en `OnboardingModels.kt`.
- Campos: `type`, `invitationToken`, `invitationType`, `versionApp`, `collectorName`, `dni`.
- Los campos son opcionales excepto `type`; la validación de campos requeridos para
  `type = "consent"` se delega al backend.

#### `OnboardingRepository` — `getLegalDocumentEncrypted`
- Nuevo método `getLegalDocumentEncrypted(type, invitationToken, invitationType, collectorName, dni)`.
- Reutiliza `getOnboardingPublicKey()` (con caché de sesión) y `encryptOnboardingPayload()`
  exactamente igual que `submitOnboarding`.
- Aplica el mismo formateo del token `SHORT_CODE` (guion en punto medio).
- Si el endpoint cifrado falla, hace **fallback automático** al endpoint GET sin cifrar.

#### `ConsentViewModel` — carga cifrada
- Eliminado el bloque `init { loadInformedConsent() }` que auto-cargaba el consentimiento
  genérico sin contexto del recolector.
- Nuevo método `loadInformedConsentEncrypted(accessCode, accessType, firstName, lastName, dni)`:
  - Mapea `accessType` → `invitationType` (`"invitation_code"` → `"SHORT_CODE"`)
  - Normaliza el nombre del recolector a mayúsculas (`collectorName`)
  - Implementa fallback a `loadInformedConsent()` si el cifrado falla.
- Se mantiene `loadInformedConsent()` como fallback interno y para tipos sin contexto
  (`privacy`, `terms`).

#### `ConsentScreen` — carga al entrar a la pantalla
- `LaunchedEffect(Unit)`: lee `accessCode` / `accessType` desde `OnboardingPreferences`
  y llama a `loadInformedConsentEncrypted` con los parámetros del recolector.
- Si `accessCode` está vacío hace fallback al método sin cifrar.
- El contenido del documento se abre en un `Dialog` de pantalla completa con:
  - Barra superior con botón de cierre (×)
  - Renderizado completo en Markdown con `Markwon` (tablas, tachado, listas, HTML, links)
  - Indicador de carga y botón "Reintentar" que respeta el flujo cifrado.

> **Importante:** el consentimiento personalizado se genera sobre la marcha a partir del token
> de invitación activo. Solo al completar el onboarding (firma + envío) se crea el registro
> del recolector en el backend.

---

## [v1.1.0] — 2026-03-30

### Novedades — Gestión de errores en registro y sincronización de actividades

#### Base de datos — Migración v8 → v9
- Añadida columna `activityId` a la tabla `photos` para vincular directamente cada foto
  con su actividad correspondiente, además del `fieldKey`.
- Las entidades `ActivityEntity` almacenan `syncRetryCount` y `lastError` para controlar
  el ciclo de vida de sincronización.

#### `ActivitiesRepository` — Política de reintentos y validación de integridad
- Actividades con **3 o más intentos fallidos** se excluyen de las sincronizaciones automáticas,
  evitando ciclos infinitos de reintentos.
- El contador `syncRetryCount` se incrementa con cada fallo, guardando `errorCode`,
  `errorMessage` y `stackTrace`.
- Antes de enviar al Service Bus, se valida que todos los archivos multimedia referenciados
  existan con sus URLs remotas.
- Implementada actualización masiva (`UPDATE`) para vincular fotos a actividades.

#### `PhotoRepository` — Corrección de fotos huérfanas
- Corregida la lógica que dejaba fotos temporales sin vincular a ninguna actividad.

#### UI — Indicadores de error en actividades
- **Lista de actividades (`TasksScreens`):** tarjetas con error muestran mensaje y contador
  de intentos (p. ej. "2 / 3") con color rojo.
- **Detalle de actividad (`ActivityDetailScreen`):** tarjeta roja con detalle técnico del error
  y sugerencias de acción al alcanzar el límite de reintentos.
- Colores de estado: 🔴 Error · 🟡 Pendiente · 🟢 Enviado.

#### Códigos de error

| Código | Descripción |
|---|---|
| `FILE_NOT_FOUND` | El archivo de la foto no existe en el dispositivo |
| `PAYLOAD_VALIDATION_ERROR` | Inconsistencia entre fotos del formulario y URLs generadas |
| `UPLOAD_ERROR` | Fallo al subir imagen a Azure Blob Storage |
| `NETWORK_ERROR` | No se pudo conectar con el Service Bus |

### Estrategia Online-First para Formularios y GeoJSON

#### `FormsRepository` y `GeoJsonRepository`
- Estrategia **Online-First**: con conexión, siempre se obtienen datos frescos del servidor
  y se actualiza el caché local; sin conexión, se usa el caché automáticamente.
- Soporte para `forceRefresh = true`.
- Fallback transparente a caché local si el servidor no está disponible.
- Compatible con API 21+ (Android 5.0+).
- Los ViewModels existentes no requirieron cambios.

---

## Versiones

| Campo | Valor |
|---|---|
| Versión base | `v1.0.2` |
| Versión intermedia | `v1.1.0` |
| Versión final | `v1.2.0` |
| Tipo de cambio | Funcionalidad nueva + correcciones |

---

## Integración — Envío de Errores a la API de Notificaciones (`/api/events-logging`)

### Resumen

La app Android envía eventos de fallo a **`pachamama-api-notifications-java`**
(`POST /api/events-logging`) con una estrategia **Online-First con fallback offline**: si hay conexión
el log se envía inmediatamente; si no la hay, se persiste localmente en Room y se reintenta de forma
automática cuando se recupera la red.

**Endpoint:**
```
POST https://pachamama-api-notif-java-6245560b7544.herokuapp.com/api/events-logging
Content-Type: application/json
```

---

### Arquitectura de la Integración

```
┌─────────────────────────────────────┐
│  FormViewModel / ActivitiesRepo     │
│  (puntos de error)                  │
└────────────────┬────────────────────┘
                 │ logError(tag, process, message, statusCode, metadata)
                 ▼
┌─────────────────────────────────────┐
│  EventLoggingRepository             │  ← @Singleton, inyectado por Hilt
│  (capa de orquestación)             │
└──────┬──────────────────┬───────────┘
       │ Online            │ Offline / Error HTTP
       ▼                   ▼
┌─────────────┐   ┌────────────────────────┐
│ POST        │   │  Room DB               │
│ /api/events │   │  tabla: event_logs     │
│ -logging    │   │  (EventLogEntity)      │
└─────────────┘   └────────────┬───────────┘
                               │ Cada 15 min (red disponible)
                               ▼
                  ┌────────────────────────┐
                  │  EventLogSyncWorker    │
                  │  (WorkManager)         │
                  │  → syncOfflineLogs()   │
                  └────────────────────────┘
```

---

### Clases Involucradas

#### `EventLoggingService` — Interfaz Retrofit

```kotlin
// data/logging/EventLoggingService.kt
interface EventLoggingService {
    @POST("api/events-logging")
    suspend fun logEvent(@Body request: EventLogRequest): Response<Unit>
}
```

- Instanciada vía `NetworkModule` con el cliente `LoggingRetrofit`.
- Sin autenticación adicional.

#### `EventLoggingRepository` — Orquestador

```kotlin
// data/logging/EventLoggingRepository.kt
fun logError(
    tag: String,
    process: String,
    message: String,
    statusCode: String,
    startTime: Long = System.currentTimeMillis(),
    endTime: Long = System.currentTimeMillis(),
    metadata: Map<String, Any> = emptyMap()
)
```

- **Fire-and-forget**: no bloquea la corrutina del caller.
- Auto-genera `traceId` (UUID), enriquece con `device` / `os` (Build.MODEL / Build.VERSION.RELEASE).
- Toma `userId`, `tenantId`, `projectId` desde `SessionPreferences`.
- Si el POST falla (red o HTTP) → `saveOfflineLog()` → INSERT en Room.

#### `EventLogEntity` / `EventLogDao` — Almacenamiento Offline

```kotlin
@Entity(tableName = "event_logs")
data class EventLogEntity(
    @PrimaryKey val traceId: String,
    val channel: String,         // siempre "app"
    val channelVersion: String,  // BuildConfig.VERSION_NAME
    val userId: String,
    val tenantId: String,
    val projectId: String,
    val onboardingId: String,    // mismo que userId
    val tag: String,
    val process: String,
    val startTime: Long,
    val endTime: Long,
    val level: String,
    val message: String,
    val statusCode: String,
    val clientIp: String,        // "0.0.0.0"
    val userAgent: String,       // "Android/{Build.VERSION.RELEASE}"
    val environment: String,     // "prod"
    val metadataString: String   // metadata serializada como JSON (Gson)
)
```

#### `EventLogSyncWorker` — Reintentos Periódicos

- Ejecuta `syncOfflineLogs()` cada **15 minutos** cuando hay red disponible.
- Backoff exponencial de 10 minutos en caso de fallo del worker.

---

### Puntos de Integración en el Código

| Clase | Método | `statusCode` | Descripción |
|---|---|---|---|
| `FormViewModel` | `saveAsPendingActivity` | `CRITICAL_ERROR` | Error crítico al guardar actividad en Room |
| `ActivitiesRepository` | `uploadMediaAndReplaceFormData` | `FILE_NOT_FOUND` | El archivo de foto no existe en el dispositivo |
| `ActivitiesRepository` | `uploadMediaAndReplaceFormData` | `UPLOAD_ERROR` | Fallo al subir imagen a Azure Blob Storage |
| `ActivitiesRepository` | `syncPendingActivities` | `FATAL_SYNC_ERROR` | Error de infraestructura al enviar al Service Bus |

---

### Ejemplo de Payload Enviado

```json
{
  "traceId":        "550e8400-e29b-41d4-a716-446655440000",
  "channel":        "app",
  "channelVersion": "1.2.0",
  "userId":         "collector-uuid",
  "tenantId":       "company-uuid",
  "projectId":      "project-uuid",
  "onboardingId":   "collector-uuid",
  "tag":            "ActivitiesRepository",
  "process":        "uploadMediaAndReplaceFormData",
  "startTime":      1744120800000,
  "endTime":        1744120801500,
  "level":          "ERROR",
  "message":        "Error en carga de archivos multimedia: file not found",
  "statusCode":     "FILE_NOT_FOUND",
  "clientIp":       "0.0.0.0",
  "userAgent":      "Android/14",
  "environment":    "prod",
  "metadata": {
    "device":      "Pixel 7",
    "os":          "14",
    "activityId":  "act-uuid",
    "errorTrace":  "java.io.FileNotFoundException: ..."
  }
}
```
