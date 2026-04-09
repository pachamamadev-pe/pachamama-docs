# Gestión de Cambios: Observación — Permisos Requeridos (Android)

## Registro de Cambios

---

## [8 – 9 Abr 2026] Protección Obligatoria de Permisos al Inicio

**Autor:** Jecri Do Santos  
**Período:** 8 – 9 de Abril 2026 *(2 días)*  
**APK generada:** `v1.2.1`

**Objetivo:** Cumplir con la observación de que los permisos no concedidos (cámara, ubicación, almacenamiento y notificaciones) bloqueaban silenciosamente el uso de la app, implementando una pantalla de bloqueo explícita que da mayor claridad y guía al recolector para resolver el problema por sí mismo.

### Contexto

Durante el uso en campo se detectó que si un recolector no había concedido los permisos necesarios, la aplicación podía fallar de forma silenciosa o con mensajes de error técnico confusos:

1. **Sin georreferenciación:** La actividad se registraba sin coordenadas válidas al no tener permiso de ubicación.
2. **Sin captura fotográfica:** La cámara no abría al no tener el permiso correspondiente, generando datos incompletos.
3. **Sin notificaciones:** El recolector no recibía alertas del sistema.

Con este cambio, la aplicación **no permite avanzar** hasta que todos los permisos indispensables sean concedidos, y guía al usuario con opciones claras para resolverlo.

---

### Componentes Modificados

| Componente | Versión | Descripción del Cambio |
|---|---|---|
| [Pachamama Mobile Android](pachamama-mobile-android.md) | `v1.2.0` → `v1.2.1` | Pantalla de bloqueo con gestión explícita de permisos obligatorios al inicio |

---

### Flujo del Cambio — Verificación de Permisos al Inicio

```
App Launch
   │  Se verifican los permisos: Cámara, Ubicación, Almacenamiento, Notificaciones
   ▼
¿Todos los permisos concedidos?
   │
   ├─ SÍ ──► La app inicia normalmente (flujo transparente al usuario)
   │
   └─ NO ──► Pantalla de bloqueo "Permisos necesarios"
                │
                ├─ Botón "Reintentar pedir Permisos"
                │    └─ Lanza el diálogo estándar de Android (si no está bloqueado)
                │
                └─ Botón "Abrir Ajustes del Sistema"
                     └─ Lleva directamente a la pantalla de permisos
                          de la app en Ajustes del teléfono
```

---

### Particularidades de Android

Las versiones modernas de Android aplican una protección contra solicitudes repetidas de permisos:

- **Primer rechazo:** La app puede volver a solicitar el permiso mediante el diálogo estándar.
- **Rechazo permanente:** Si el usuario marca *"No volver a preguntar"* o rechaza por segunda vez, Android oculta definitivamente el diálogo para esa app. La única salida es ir manualmente a los **Ajustes del sistema**.

Por eso la pantalla de bloqueo incorpora ambos botones como solución a prueba de fallos: si el primero no hace nada (señal de que el bloqueo es permanente), el segundo lleva directamente a la pantalla exacta en Ajustes.

---

### Beneficios

| Indicador | Descripción |
|---|---|
| **Calidad de datos** | Garantiza que ninguna actividad se registre sin capacidad de tomar foto o georreferenciar |
| **Soporte reducido** | El recolector puede resolver el problema por sí mismo sin asistencia técnica |
| **Transparencia** | El usuario entiende explícitamente por qué la app no avanza |
