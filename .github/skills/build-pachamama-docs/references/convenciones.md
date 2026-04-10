> Referencia del skill `pachamama-docs` — Convenciones del Proyecto

# Convenciones del Proyecto Pachamama

## Datos del Proyecto

| Campo | Valor |
|-------|-------|
| Empresa | REORI CORP S.A.C. |
| Producto | Pachamama |
| Autor principal | Jecri Do Santos |
| Tenant Azure corporativo | `pachamamadev@pachamaxter.onmicrosoft.com` |
| Region Azure objetivo | `brazilsouth` |
| Resource Group producción | `rg-pachamama-prd-eastus` (transitorio → migrar a brazilsouth) |

---

## Convenciones de Nomenclatura

### Slugs de Carpetas (`gestion-cambios/`)

```
Regla:   kebab-case, minúsculas, sin tildes ni caracteres especiales
Formato: <descripcion-corta-del-cambio>

Ejemplos correctos:
  validacion-otp-campo
  permisos-requeridos
  sincronizar-actividades-kpi
  consentimiento-informado-cifrado

Ejemplos incorrectos:
  ValidacionOTP           ← PascalCase no permitido
  validacion_otp_campo    ← snake_case no permitido
  validación-otp          ← con tilde no permitido
```

### Nombres de Archivo de Servicios

```
Regla general: <clave-de-servicio>.md
Excepción:     pachamama-web-admin → pachamama-admin-web.md
```

| Servicio | Nombre de archivo |
|----------|------------------|
| `pachamama-mobile-android` | `pachamama-mobile-android.md` |
| `pachamama-api-admin-java` | `pachamama-api-admin-java.md` |
| `pachamama-api-sync-java` | `pachamama-api-sync-java.md` |
| `pachamama-api-notifications-java` | `pachamama-api-notifications-java.md` |
| `pachamama-api-trace-java` | `pachamama-api-trace-java.md` |
| `pachamama-web-admin` | `pachamama-admin-web.md` ⚠️ |

### Archivos de Arquitectura

```
Formato:  ARQ-<PROYECTO>-<PROVEEDOR>-<YYYYMMDD>.md        ← versión inicial
Revisión: ARQ-<PROYECTO>-<PROVEEDOR>-<YYYYMMDD>-v2.md     ← revisión 2
          ARQ-<PROYECTO>-<PROVEEDOR>-<YYYYMMDD>-v3.md     ← revisión 3

Proyectos en uso:
  PACHAMAMA

Proveedores en uso:
  AZURE

Ejemplos:
  ARQ-PACHAMAMA-AZURE-20260410.md
  ARQ-PACHAMAMA-AZURE-FULL-20260410.md
  ARQ-PACHAMAMA-AZURE-FULL-20260410-v2.md
```

---

## Convenciones de Fechas

### En títulos de Gestión de Cambios

```
Formato estándar:  DD-DD Mmm YYYY
Formato multi-mes: DD Mmm – DD Mmm YYYY

Ejemplos:
  8-9 Abr 2026
  15-20 May 2026
  28 Abr – 2 May 2026
```

### En entradas de `mkdocs.yml`

```yaml
"[8-9 Abr 2026] Permisos Requeridos (Android)"
"[15-20 May 2026] Validación OTP en Campo"
"[28 Abr – 2 May 2026] Consentimiento Informado Cifrado"
```

### En headers de archivos Markdown

```markdown
**Período:** 8 de Abril – 9 de Abril 2026 *(2 días)*
**Período:** 15 – 20 de Mayo 2026 *(6 días)*
```

### En `cambios-app.txt`

```
Estos cambios (v1.2.1) se hicieron el 8-9 de Abril de 2026
```

### En changelogs de servicio (sección `## [vX.Y.Z]`)

```markdown
## [1.2.1] — 2026-04-09
```

ISO 8601 (`YYYY-MM-DD`) para las fechas dentro de changelogs de servicio.

---

## Convenciones de Versiones

### Mobile Android

```
Esquema:   MAJOR.MINOR.PATCH
Ejemplos:  1.2.0, 1.2.1, 1.3.0

Cuándo incrementar:
  MAJOR  → Cambio arquitectónico mayor o rebranding
  MINOR  → Nueva funcionalidad completa
  PATCH  → Corrección de bugs u observaciones puntuales
```

### APIs Java (Heroku / Azure)

```
Esquema:   MAJOR.MINOR.PATCH
Manejo:    Definido por el build de Heroku/Maven
```

---

## Convenciones de Diagramas

```
Regla: Siempre usar Mermaid para diagramas técnicos
       Nunca ASCII puro para diagramas complejos

Tipos de diagrama usados:
  flowchart TD / LR   ← Flujos de proceso
  sequenceDiagram     ← Flujos de comunicación entre servicios
  graph               ← Topología de infraestructura
```

---

## Convenciones de Títulos en Secciones

### En `index.md` de Gestión de Cambios

```markdown
# Gestión de Cambios: <Observación/Feature — Nombre>

## Registro de Cambios

## [DD Mmm – DD Mmm YYYY] <Nombre Corto>

### Contexto
### Componentes Modificados
### Flujo del Cambio — <Nombre>
### Particularidades Técnicas
```

### En `<servicio>.md` de Gestión de Cambios

```markdown
# Changelog — <Nombre Legible del Servicio>

## [vX.Y.Z] — YYYY-MM-DD

### <Categoría> — <Nombre del Sub-cambio>

#### <Componente o Endpoint>
```

---

## Orden de Entradas en `mkdocs.yml`

Siempre insertar **al inicio** de la sección correspondiente (orden cronológico descendente — más reciente primero).

```yaml
- Gestión de Cambios:
  - "[20-25 Jun 2026] Cambio más reciente":   # ← NUEVO va aquí
    - Resumen Integral: gestion-cambios/cambio-reciente/index.md
  - "[8-9 Abr 2026] Permisos Requeridos (Android)":  # ← existente
    - Resumen Integral: gestion-cambios/permisos-requeridos/index.md
    - Mobile Android: gestion-cambios/permisos-requeridos/pachamama-mobile-android.md
```

---

## Regla de `cambios-app.txt`

Actualizar **sólo cuando** `pachamama-mobile-android` esté afectado.  
Insertar al **inicio** del archivo, no al final.

```
Estos cambios (vX.Y.Z) se hicieron el DD-DD de Mes de YYYY

## [X.Y.Z] — YYYY-MM-DD

### <Categoría> — <Nombre del Cambio>

- Descripción bullet del cambio mobile.
- Otro bullet si aplica.
```
