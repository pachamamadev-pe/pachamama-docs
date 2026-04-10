# Changelog — Pachamama Mobile Android

**Versiones:** `v1.2.1` → `v1.2.2`
**Cambio Relacionado:** Validación de Conectividad y Robustez de Sincronización
**Período:** 10 de Abril 2026

---

## [1.2.2] — 2026-04-10

### Fixed — Validación Estricta de Conectividad a Internet (IsOnline)

#### ConnectivityManager / IsOnlineChecker
- Se reemplazó la validación de red por verificación explícita de `NET_CAPABILITY_VALIDATED` de Android. Ahora no basta estar conectado a WiFi o datos; el SO confirma que hay salida efectiva a internet antes de intentar cualquier sincronización.
- Pantallas como "Historial de Actividades" realizan consulta síncrona al sensor de red al abrirse. Si no hay internet en ese momento, abortan la consulta inmediatamente y muestran pantalla amigable de "Sin conexión".
- Se implementó UI reactiva: cuando la señal regresa, los llamados pendientes se ejecutan automáticamente sin intervención del usuario.

### Fixed — Sincronización Ininterrumpida y Resiliente

#### SyncRepository / ServiceBusDispatcher
- El flujo de envío al Service Bus ahora envuelve las transacciones en 3 reintentos rápidos asíncronos internos, absorbiendo fluctuaciones breves de red (`SocketException`, `Connection reset`) sin interrumpir el proceso general de sincronización.
- Se eliminó la restricción de intentos máximos `(n/3)`. El botón "Sincronizar Todo" ya no se bloquea permanentemente tras múltiples fallos de red; el usuario siempre puede reintentar.

#### SyncWorker / CoroutineScope
- Se agregó blindaje `NonCancellable` en el scope de sincronización. Si Android cancela el proceso en background, la actividad es forzosamente regresada al estado `ERROR` (nunca queda bloqueada en `SYNCING`), permitiendo que sea detectada y reintentada en el siguiente ciclo.

### Changed — Telemetría y Categorización de Errores

#### ErrorLogger / SyncTelemetry
- Nuevo metadato `syncSource` en reportes de error: indica si el fallo ocurrió por acción `MANUAL` (usuario tocó el botón) o `WORKER` (tarea automatizada en background), mejorando el diagnóstico operativo.
- Los errores de red temporales (`Connection reset`, `SocketException`) se etiquetan explícitamente como `NETWORK_ERROR` en telemetría, separándolos de `FATAL_SYNC_ERROR` (fallos de servicios centrales o datos corruptos).

---

## [1.2.1] — 2026-04-09

### Versión anterior

Ver detalle completo en:
[Permisos Requeridos (Android)](../permisos-requeridos/pachamama-mobile-android.md)
