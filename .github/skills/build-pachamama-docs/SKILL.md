---
name: build-pachamama-docs
description: "Skill especializado en el repositorio de documentación Pachamama (REORI CORP S.A.C.). Usar cuando el usuario solicite: agregar un cambio de funcionalidad, registrar una nueva observación, documentar un servicio, actualizar infraestructura, crear un flujo arquitectónico, agregar cualquier contenido a este repositorio, o reestructurar un documento existente. El skill identifica la sección correcta, genera los archivos necesarios, actualiza mkdocs.yml, y hace las preguntas adecuadas si falta información."
---

# Pachamama Docs — Skill de Documentación

## Referencias de Conocimiento

Cargar según el tipo de operación solicitada:

| Referencia | Cuándo cargar |
|-----------|--------------|
| [estructura-repo.md](./references/estructura-repo.md) | Para cualquier operación — describe el árbol completo y las secciones del repo |
| [servicios.md](./references/servicios.md) | Cuando el cambio afecta uno o más servicios — tabla de nombres, claves y relaciones |
| [convenciones.md](./references/convenciones.md) | Para slugs, fechas, versiones, nav mkdocs, y reglas de nomenclatura |
| [contexto-sistema.md](./references/contexto-sistema.md) | Para entender el sistema Pachamama, el stack y la migración Azure planificada |

## Plantillas de Documentación

| Plantilla | Para qué usarla |
|-----------|----------------|
| [gestion-cambios-index.md](./templates/gestion-cambios-index.md) | Resumen integral de un cambio funcional (`index.md`) |
| [gestion-cambios-servicio.md](./templates/gestion-cambios-servicio.md) | Changelog detallado de un servicio afectado por un cambio |
| [flujo-arquitectonico.md](./templates/flujo-arquitectonico.md) | Flujo técnico del sistema con diagrama Mermaid |
| [servicio-readme.md](./templates/servicio-readme.md) | README de un servicio bajo `docs/services/` |
| [infraestructura.md](./templates/infraestructura.md) | Documentación de un proveedor bajo `docs/infrastructure/` |

---

## Tipos de Operación

### Paso 1 — Identificar el tipo de contenido

```
¿Qué quiere el usuario?
│
├─ Agregar cambio / feature / observación    → Tipo 1: Gestión de Cambios
├─ Actualizar proveedor o cuenta cloud       → Tipo 2: Infraestructura
├─ Crear o actualizar flujo técnico          → Tipo 3: Flujos Arquitectónicos
├─ Actualizar info de un servicio            → Tipo 4: Servicios
├─ Crear documento de arquitectura formal    → Tipo 5: Arquitecturas
├─ Actualizar referencia técnica             → Tipo 6: Referencias
└─ Reestructurar documento existente         → Tipo 7: Reestructuración
```

---

## Tipo 1 — Gestión de Cambios

Cargar: [estructura-repo.md](./references/estructura-repo.md), [servicios.md](./references/servicios.md), [convenciones.md](./references/convenciones.md)  
Plantillas: [gestion-cambios-index.md](./templates/gestion-cambios-index.md), [gestion-cambios-servicio.md](./templates/gestion-cambios-servicio.md)

### Preguntas obligatorias

| # | Pregunta | Necesario para |
|---|----------|---------------|
| Q1 | **¿Nombre del cambio?** (descripción corta, ej: "Validación OTP en campo") | slug de carpeta y título nav |
| Q2 | **¿Rango de fechas?** (ej: "15-20 May 2026") | header `index.md` y entrada nav |
| Q3 | **¿Qué servicios fueron afectados?** | qué archivos `<servicio>.md` crear |
| Q4 | **¿El autor?** | header `index.md` |
| Q5 | **¿Nueva versión de APK?** y ¿cuál? | solo si mobile está afectado |
| Q6 | **¿Cuál fue el objetivo u observación original?** | sección Objetivo y Contexto |
| Q7 | **¿Qué cambió exactamente en cada servicio?** | cuerpo de cada `<servicio>.md` |

> Si el usuario provee un documento adjunto con los cambios, extraer Q1–Q7 del documento antes de preguntar.

### Archivos a crear / modificar

| Acción | Archivo |
|--------|---------|
| Crear | `docs/gestion-cambios/<slug>/index.md` |
| Crear | `docs/gestion-cambios/<slug>/<servicio>.md` × 1 por servicio afectado |
| Modificar | `mkdocs.yml` — agregar al inicio de "Gestión de Cambios" |
| Modificar | `docs/referencias/cambios-app.txt` — solo si mobile fue afectado |

---

## Tipo 2 — Infraestructura

Cargar: [estructura-repo.md](./references/estructura-repo.md), [contexto-sistema.md](./references/contexto-sistema.md)  
Plantilla: [infraestructura.md](./templates/infraestructura.md)

### Preguntas obligatorias

| # | Pregunta |
|---|----------|
| Q1 | **¿Qué proveedor?** (azure, heroku, railway, mongodb, redis, firebase, vercel, twilio) |
| Q2 | **¿Qué cambió?** (cuenta, recursos, topología, SKUs, precios) |
| Q3 | **¿Se debe regenerar el diagrama Mermaid de topología?** |

### Archivos a modificar

- `docs/infrastructure/<proveedor>.md` — edición directa

---

## Tipo 3 — Flujos Arquitectónicos

Cargar: [estructura-repo.md](./references/estructura-repo.md), [servicios.md](./references/servicios.md)  
Plantilla: [flujo-arquitectonico.md](./templates/flujo-arquitectonico.md)

### Preguntas obligatorias

| # | Pregunta |
|---|----------|
| Q1 | **¿Nombre del flujo?** (ej: "Autenticación OTP") |
| Q2 | **¿Qué servicios participan?** |
| Q3 | **¿Es nuevo o actualización de uno existente?** |
| Q4 | **¿Se provee diagrama Mermaid o se debe generar?** |

### Archivos

- **Nuevo**: `docs/flujos/<slug>.md` + entrada en `mkdocs.yml` bajo "Flujos Arquitectónicos"
- **Editar**: `docs/flujos/<nombre>.md` existente

---

## Tipo 4 — Servicios (README)

Cargar: [servicios.md](./references/servicios.md)  
Plantilla: [servicio-readme.md](./templates/servicio-readme.md)

### Preguntas obligatorias

| # | Pregunta |
|---|----------|
| Q1 | **¿Qué servicio?** (ver tabla en servicios.md) |
| Q2 | **¿Qué aspecto se actualiza?** (stack, integraciones, distribución, arquitectura interna) |

### Archivo

- `docs/services/<nombre>/README.md`

---

## Tipo 5 — Arquitecturas

Cargar: [contexto-sistema.md](./references/contexto-sistema.md)  
Usar en conjunto con el skill `arquitecto-cloud` para el contenido.

### Preguntas obligatorias

| # | Pregunta |
|---|----------|
| Q1 | **¿Nueva arquitectura o revisión de una existente?** |
| Q2 | **¿Cuál es el alcance?** (Fase 1, migración completa, un servicio) |
| Q3 | **¿Hay documento previo a referenciar?** |

### Naming de archivo

```
ARQ-<PROYECTO>-<PROVEEDOR>-<YYYYMMDD>.md       ← versión inicial
ARQ-<PROYECTO>-<PROVEEDOR>-<YYYYMMDD>-v2.md    ← revisiones
```

---

## Tipo 6 — Referencias Técnicas

Cargar: [estructura-repo.md](./references/estructura-repo.md)

### Sub-tipos

| Sub-tipo | Ruta | Cuándo |
|----------|------|--------|
| Changelog master móvil | `docs/referencias/cambios-app.txt` | Agregar al inicio en CADA cambio mobile |
| Changelog de impl. detallado | `docs/referencias/cambios-en-implementacion/<feature>/changelog-<servicio>.md` | Changelogs técnicos durante desarrollo |
| Config dumps `.txt` | `docs/referencias/*.txt` | Logs/dumps de recursos cloud |

---

## Tipo 7 — Reestructuración de Documento Existente

Cargar: todas las referencias y la plantilla correspondiente al tipo detectado.

### ¿Qué es?
Proceso para tomar un documento existente que no sigue la estructura correcta y reformatearlo/reorganizarlo según las plantillas del repositorio, **sin perder información**.

### Paso a paso

```
1. Leer el documento existente completo
2. Identificar a qué Tipo pertenece (1–6)
3. Cargar la plantilla correspondiente
4. Mapear: sección actual → sección de la plantilla
5. Identificar información faltante → preguntar al usuario
6. Generar el documento reestructurado
7. Confirmar con el usuario antes de sobreescribir el original
```

### Mapeo por Tipo al reestructurar

**Tipo 1 — Gestión de Cambios (`index.md`)**

| Buscar en el doc actual | Mapea a sección de plantilla |
|------------------------|------------------------------|
| Fechas / período | Header `[DD Mmm – DD Mmm YYYY]` |
| Descripción del problema | Sección `Contexto` |
| Componentes / servicios tocados | Tabla `Componentes Modificados` |
| Flujo descrito en prosa | Sección `Flujo del Cambio` (convertir a diagrama) |
| Notas técnicas sueltas | Sección `Particularidades` |
| APK / versión mencionada | Campo `APK generada` en header |

**Tipo 1 — Gestión de Cambios (`<servicio>.md`)**

| Buscar en el doc actual | Mapea a sección de plantilla |
|------------------------|------------------------------|
| Título / nombre del servicio | Header `# Changelog — <Nombre>` |
| Versión anterior y nueva | `**Versiones:** vX → vX` |
| Lista de cambios | Bullets bajo `## [vX.Y.Z]` agrupados por categoría |
| Referencia a cambio anterior | Sección `## [vX-anterior] — Versión anterior` |

**Tipo 2 — Infraestructura**

| Buscar en el doc actual | Mapea a sección de plantilla |
|------------------------|------------------------------|
| Datos de cuenta/tenant | Sección `Detalles de Cuenta y Entorno` |
| Recursos listados | Tabla `Servicios Activos` |
| Diagrama de recursos | Sección `Topología de Recursos` (Mermaid) |

**Tipo 3 — Flujo Arquitectónico**

| Buscar en el doc actual | Mapea a sección de plantilla |
|------------------------|------------------------------|
| Descripción del flujo | Párrafo introductorio |
| Diagrama existente (ASCII/Mermaid) | Sección `Diagrama de <Nombre>` |
| Pasos enumerados | Sección `Resumen Operativo` |
| Notas técnicas | Sección `Notas Técnicas` |

### Checklist de reestructuración

- [ ] ¿Toda la información del documento original quedó mapeada? (nada se pierde)
- [ ] ¿El encabezado tiene todos los campos requeridos por la plantilla?
- [ ] ¿Los diagramas ASCII fueron convertidos a Mermaid?
- [ ] ¿El archivo está en la ruta correcta según su tipo?
- [ ] ¿Se actualizó `mkdocs.yml` si el archivo cambió de ruta?
- [ ] ¿Se confirmó con el usuario antes de sobreescribir?

---

## Regla de Actualización de `mkdocs.yml`

Obligatorio para Tipos 1, 3 y cualquier archivo nuevo.

```yaml
# Patrón en Gestión de Cambios (orden: más reciente primero)
- "[DD-DD Mmm YYYY] Nombre del Cambio":
  - Resumen Integral: gestion-cambios/<slug>/index.md
  - <Nombre Servicio>: gestion-cambios/<slug>/<servicio>.md
```

---

## Regla de Actualización de `cambios-app.txt`

Solo cuando `pachamama-mobile-android` está afectado. Insertar al **inicio** del archivo:

```
Estos cambios (v<X.Y.Z>) se hicieron el <fecha>

## [<X.Y.Z>] — YYYY-MM-DD

### <Categoría> — <Nombre del cambio>

- Bullet del cambio implementado.
```
