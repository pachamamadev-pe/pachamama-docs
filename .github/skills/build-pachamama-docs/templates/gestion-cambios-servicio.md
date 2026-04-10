> Plantilla del skill `pachamama-docs` — Gestión de Cambios: `<servicio>.md`

---

```markdown
# Changelog — [NOMBRE_LEGIBLE_DEL_SERVICIO]

**Versiones:** `v[X.Y.Z-ANTES]` → `v[X.Y.Z-DESPUES]`
**Cambio Relacionado:** [Nombre del cambio / observación]
**Período:** [DD] – [DD] de [Mes] [YYYY]

---

## [v[X.Y.Z-DESPUES]] — [YYYY-MM-DD]

### [CATEGORIA] — [NOMBRE_DEL_SUBAMBIO]

#### [COMPONENTE_O_ENDPOINT_1]
- [Descripción bullet del cambio implementado.]
- [Otro bullet de detalle técnico si aplica.]

#### [COMPONENTE_O_ENDPOINT_2]
- [Descripción bullet del cambio.]

<!-- Agregar tantas sub-secciones como componentes o endpoints modificados -->

---

## [v[X.Y.Z-ANTES]] — [YYYY-MM-DD-ANTERIOR]

### Versión anterior

Ver detalle completo en:
[[Nombre del cambio anterior]](../<carpeta-cambio-anterior>/<servicio>.md)
```

---

## Campos Obligatorios

| Campo | Notas |
|-------|-------|
| `# Changelog — <Nombre>` | Nombre legible del servicio (no la clave técnica) |
| `**Versiones:**` | La versión anterior y la nueva en formato `v[X] → v[X]` |
| `**Cambio Relacionado:**` | Nombre del cambio al que pertenece este changelog |
| `**Período:**` | Rango de fechas del cambio |
| `## [vX.Y.Z]` | Sección de la versión nueva (con ISO date) |
| `### <Categoría>` | Al menos una categoría de cambio |
| `## [vX.Y.Z-anterior]` | Sección de versión anterior con link a changelog previo |

---

## Categorías de Cambio Recomendadas

```
### Added — [Nombre]        ← Funcionalidades nuevas
### Changed — [Nombre]      ← Cambios en funcionalidad existente
### Fixed — [Nombre]        ← Correcciones de bugs u observaciones
### Removed — [Nombre]      ← Funcionalidades eliminadas
### Security — [Nombre]     ← Cambios relacionados con seguridad
### Refactored — [Nombre]   ← Refactoring sin cambio de comportamiento
```

---

## Nombres Legibles por Servicio

| Clave de servicio | Nombre en `# Changelog —` |
|------------------|-----------------------------|
| `pachamama-mobile-android` | `Pachamama Mobile Android` |
| `pachamama-api-admin-java` | `Pachamama API Admin Java` |
| `pachamama-api-sync-java` | `Pachamama API Sync Java` |
| `pachamama-api-notifications-java` | `Pachamama API Notifications Java` |
| `pachamama-api-trace-java` | `Pachamama API Trace Java` |
| `pachamama-web-admin` | `Pachamama Admin Web` |

---

## Ejemplo Completo — Mobile Android

```markdown
# Changelog — Pachamama Mobile Android

**Versiones:** `v1.2.0` → `v1.2.1`
**Cambio Relacionado:** Permisos Requeridos (Android)
**Período:** 8 – 9 de Abril 2026

---

## [1.2.1] — 2026-04-09

### Added — Pantalla de Permisos Bloqueados

#### PermissionsBlockedScreen
- Se agregó nueva pantalla `PermissionsBlockedScreen` que se muestra cuando
  el usuario deniega permisos requeridos (cámara, ubicación, almacenamiento).
- La pantalla incluye mensaje descriptivo y botón para abrir Configuración del sistema.
- Se integró validación al inicio de flujos que requieren permisos críticos.

#### PermissionsManager
- Nuevo componente `PermissionsManager` que centraliza la verificación de permisos
  en tiempo de ejecución.
- Maneja los tres estados: `GRANTED`, `DENIED`, `PERMANENTLY_DENIED`.

---

## [1.2.0] — 2026-04-01

### Versión anterior

Ver detalle completo en:
[Trazabilidad de Versión de App](../trazabilidad-app-version/pachamama-mobile-android.md)
```

---

## Ejemplo Completo — API Admin Java

```markdown
# Changelog — Pachamama API Admin Java

**Versiones:** `v3.1.0` → `v3.1.1`
**Cambio Relacionado:** Validación OTP en Campo
**Período:** 15 – 20 de Mayo 2026

---

## [3.1.1] — 2026-05-20

### Added — Endpoint de Validación OTP

#### POST /api/v1/otp/validate
- Nuevo endpoint para validar OTP recibido vía Twilio WhatsApp.
- Requiere `brigadistaId` y `otpCode` en el body.
- Retorna `200 OK` con token temporal de 15min o `400 Bad Request` si OTP inválido.

### Changed — Configuración de Twilio

#### TwilioConfig
- Se movió la configuración de Twilio a variables de entorno para cumplir 
  buenas prácticas de seguridad.

---

## [3.1.0] — 2026-05-01

### Versión anterior

Ver detalle completo en:
[KPI Sincronización](../observacion-kpi-sincronizacion/pachamama-api-admin-java.md)
```
