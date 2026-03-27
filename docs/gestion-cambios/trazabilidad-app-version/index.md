# Gestión de Cambios: Trazabilidad de Versión de App en Actividades

## Registro de Cambios

---

## [26 – 27 Mar 2026] Visualización de Versión de App en Actividades

**Autor:** Jecri Do Santos  
**Período:** 26 – 27 de Marzo 2026 *(2 días)*  
**APK generada:** `v1.0.2`

**Objetivo:** Cumplir con la solicitud de negocio de *"visualizar la versión de la aplicación móvil con la que se registran las actividades"*, permitiendo trazabilidad y diagnóstico de registros de campo.

### Contexto

Desde el área de negocio se solicitó disponer de la versión exacta de la app móvil utilizada al momento de registrar cada actividad, con el fin de:

1. **Facilitar el diagnóstico** de incidencias reportadas, identificando qué versión de la app estaba en uso durante el registro.
2. **Mejorar la trazabilidad** del ciclo de vida de las actividades, correlacionando cambios de comportamiento con versiones específicas del cliente móvil.

---

### Componentes Modificados

| Componente | Descripción del Cambio |
|---|---|
| `pachamama-data-dll` | Adición de columna `app_version` en las tablas relacionadas a actividades |
| [Pachamama Mobile Android](pachamama-mobile-android.md) `v1.0.2` | Envío del campo `app_version` en el payload de sincronización |
| [Pachamama API Sync (Java)](pachamama-api-sync-java.md) | Recepción y persistencia de `app_version` al registrar la sincronización |
| [Pachamama API Admin (Java)](pachamama-api-admin-java.md) | Exposición de `app_version` en los endpoints de detalle de actividad |
| [Pachamama Admin Web](pachamama-admin-web.md) | Visualización de `app_version` en el detalle de actividad del panel administrativo |

---

### Flujo del Cambio

```
Mobile Android (v1.0.2)
   │  Envía app_version en payload de sincronización
   ▼
API Sync (Java)
   │  Recibe y persiste app_version en base de datos
   ▼
Base de Datos (pachamama-data-dll)
   │  Columna app_version en tablas de actividades
   ▼
API Admin (Java)
   │  Expone app_version en endpoint de detalle de actividad
   ▼
Admin Web
   └─ Muestra app_version en la vista de detalle de actividad
```

---

### Conclusión y Resultados

Con esta implementación, cada actividad registrada queda asociada a la versión exacta de la app con la que fue capturada. Esto habilita al equipo técnico y de negocio para realizar trazabilidad histórica, identificar regresiones relacionadas con versiones específicas y mejorar el soporte al usuario de campo.

#### Resultados Obtenidos

| Indicador | Valor |
|---|---|
| Período de implementación | 26 – 27 de Marzo 2026 |
| Duración total | 2 días |
| Versión APK generada | `v1.0.2` |
| Campo añadido en BD | `app_version` |
| Componentes actualizados | 5 (BD, Mobile, API Sync, API Admin, Web Admin) |
