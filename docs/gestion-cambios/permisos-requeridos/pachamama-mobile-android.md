# Changelog — Pachamama Mobile Android

**Versiones:** `v1.2.0` → `v1.2.1`  
**Cambio Relacionado:** Observación — Permisos Requeridos  
**Período:** 8 – 9 de Abril 2026

---

## [v1.2.1] — 2026-04-09

### Correcciones — Protección obligatoria de permisos al inicio

#### Verificación de permisos al arrancar la app
- Implementada verificación obligatoria de permisos al inicio de la aplicación:
  **Cámara**, **Ubicación precisa**, **Almacenamiento** y **Notificaciones**.
- Si todos los permisos están concedidos, la aplicación inicia con normalidad de forma
  completamente transparente para el recolector.
- Si algún permiso falta, la aplicación **no avanza** y muestra la pantalla de bloqueo
  `"Permisos necesarios"` en lugar del flujo normal.

#### Nueva pantalla — `PermissionsBlockedScreen`
- Pantalla de bloqueo con mensaje explicativo que informa al recolector por qué la app
  no puede continuar.
- Botón **"Reintentar pedir Permisos"**: lanza el diálogo estándar de Android para
  solicitar los permisos pendientes. Funciona cuando el usuario no ha bloqueado
  permanentemente la solicitud.
- Botón **"Abrir Ajustes del Sistema"**: lleva directamente a la pantalla de permisos
  de la aplicación en los Ajustes del teléfono. Se activa como segunda salida cuando
  Android ya no muestra el diálogo (bloqueo permanente por rechazo previo o por marcar
  *"No volver a preguntar"*).

#### Comportamiento ante el rechazo permanente de Android
- Si el usuario rechazó el permiso una segunda vez o marcó *"No volver a preguntar"*,
  Android oculta definitivamente el diálogo para esa aplicación.
- El botón *"Reintentar"* no producirá ninguna acción visible en ese caso; es la señal
  al usuario de que debe usar *"Abrir Ajustes del Sistema"* para activarlos manualmente.
- Este diseño a prueba de fallos cubre ambos escenarios sin requerir lógica condicional
  compleja en la UI.

---

## [v1.2.0] — 2026-04-08

### Versión anterior

Ver detalle completo en:
[gestion-cambios/consentimiento-informado-cifrado/pachamama-mobile-android.md](../consentimiento-informado-cifrado/pachamama-mobile-android.md)
