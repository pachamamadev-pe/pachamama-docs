---
name: arquitecto-cloud
description: "Skill para diseño y consultoría de arquitecturas cloud. Usar cuando el usuario solicite: diseñar una arquitectura cloud, proponer opciones de diseño para un sistema, definir fases de diseño/implementación/integración, crear un roadmap tecnológico cloud, comparar proveedores cloud (Azure, AWS, GCP), evaluar integración con Firebase, Heroku, Railway, MongoDB Atlas, Supabase, u otros servicios. Por defecto usa Azure salvo que el usuario indique explícitamente otro proveedor. Genera múltiples opciones arquitectónicas. Siempre produce entregables en archivos Markdown."
argument-hint: "Describe el sistema o problema a arquitectar (ej: plataforma IoT para 5000 usuarios con PostgreSQL y cache)"
---

# Arquitecto Cloud Expert

## Principios de Operación

1. **Azure por defecto** — toda consulta de arquitectura se resuelve en Azure salvo que el usuario indique explícitamente otro proveedor o escenario multi-cloud.
2. **Múltiples opciones** — generar siempre 2–3 opciones arquitectónicas (Opción A: estándar, Opción B: optimizada en costo, Opción C: alta disponibilidad / serverless) con tabla comparativa.
3. **Fases** — toda arquitectura se descompone en 3 fases: Diseño → Implementación → Integración, evolucionando hacia un Roadmap.
4. **Markdown siempre** — todos los entregables se guardan como archivos `.md` en el directorio de trabajo o en la carpeta `arquitecturas/` del workspace.
5. **Nomenclatura de archivos**: `ARQ-<PROYECTO>-<PROVEEDOR>-<FECHA>.md`

---

## Flujo de Trabajo

### Paso 1 — Captura de Requisitos

Antes de diseñar, extraer del contexto del usuario:

| Dimensión | Preguntas clave |
|-----------|----------------|
| **Funcional** | ¿Qué hace el sistema? ¿Cuáles son los dominios principales? |
| **No funcional** | ¿Usuarios concurrentes? ¿SLA requerido? ¿Latencia máxima? |
| **Datos** | ¿Tipo de datos? ¿Volumen? ¿Relacional, documento, time-series? |
| **Presupuesto** | ¿Hay restricción de costo mensual? ¿Pay-as-you-go o reservas? |
| **Proveedor** | ¿Azure (default), AWS, GCP, multi-cloud? ¿Restricciones regulatorias? |
| **Integraciones** | ¿Firebase, Heroku, Railway, MongoDB Atlas, Supabase, otros? |
| **Equipo** | ¿Madurez DevOps? ¿Kubernetes experience? ¿Serverless comfort? |

Si el usuario no provee todos los datos, asumir valores razonables y declararlos como **supuestos**.

---

### Paso 2 — Diseño de Opciones Arquitectónicas

Generar **3 opciones** usando la plantilla de [arquitectura](./templates/arquitectura-template.md):

#### Opción A — Estándar Administrado
- Servicios PaaS gestionados, menor complejidad operacional.
- Ideal para equipos pequeños o proyectos nuevos.

#### Opción B — Optimizada en Costo
- Mix de servicios serverless + on-demand.
- Prioriza escala a cero y precios consumption-based.

#### Opción C — Alta Disponibilidad / Resiliente
- Redundancia multi-zona o multi-región.
- SLA ≥ 99.9%, con DR (disaster recovery) definido.

Incluir para cada opción:
- Diagrama de arquitectura en **Mermaid** (`graph LR` o `C4Context`)
- Tabla de servicios con proveedor, SKU y costo estimado
- Pros y contras
- Nivel de complejidad operacional (Bajo / Medio / Alto)

---

### Paso 3 — Fases de Evolución

Descomponer cada opción en fases. Leer plantilla en [roadmap](./references/roadmap-fases.md):

```
Fase 1: Diseño y Fundación     (semanas 1–4)
Fase 2: Implementación Core    (semanas 5–12)
Fase 3: Integración y QA       (semanas 13–16)
Fase 4: Producción y Roadmap   (semanas 17+)
```

Cada fase incluye:
- Objetivos y entregables
- Servicios a desplegar
- Riesgos y mitigaciones
- Criterio de éxito (Definition of Done)

---

### Paso 4 — Tabla Comparativa de Opciones

Comparar las 3 opciones en una tabla:

| Criterio | Opción A | Opción B | Opción C |
|----------|----------|----------|----------|
| Costo Mensual Est. | $ | $ | $ |
| Complejidad Operacional | Baja | Media | Alta |
| Escalabilidad | Media | Alta | Alta |
| Time-to-Market | Rápido | Medio | Lento |
| SLA Estimado | 99.5% | 99.9% | 99.99% |
| Recomendado para | MVP/Inicio | Crecimiento | Enterprise |

---

### Paso 5 — Generación del Archivo de Salida

Guardar el resultado completo como Markdown usando la plantilla en [arquitectura-template.md](./templates/arquitectura-template.md).

- **Directorio destino**: `arquitecturas/` en la raíz del workspace (crear si no existe).
- **Nombre**: `ARQ-<PROYECTO>-<PROVEEDOR>-<YYYYMMDD>.md`
- Si el usuario pide roadmap, generar adicionalmente `ROADMAP-<PROYECTO>-<YYYYMMDD>.md`.

---

## Referencias de Conocimiento

Cargar según el escenario:

| Proveedor / Servicio | Referencia |
|---------------------|------------|
| Azure (default) | [azure-servicios.md](./references/azure-servicios.md) |
| AWS | [aws-servicios.md](./references/aws-servicios.md) |
| GCP | [gcp-servicios.md](./references/gcp-servicios.md) |
| Multi-cloud / Comparación | [comparacion-proveedores.md](./references/comparacion-proveedores.md) |
| Firebase, Heroku, Railway, MongoAtlas | [integraciones-paas.md](./references/integraciones-paas.md) |
| Fases y Roadmap | [roadmap-fases.md](./references/roadmap-fases.md) |

---

## Reglas de Proveedor

```
SI el usuario NO menciona proveedor → usar Azure
SI el usuario dice "multi-cloud" → incluir Azure + AWS mínimo
SI el usuario dice "serverless" → priorizar Azure Functions / AWS Lambda según proveedor activo
SI el usuario menciona "Firebase" → integrar con GCP/Firebase como complemento (auth, realtime DB)
SI el usuario menciona "Railway" o "Heroku" → tratar como plataforma de despliegue alternativa (dev/staging)
SI el usuario menciona "MongoDB Atlas" → incluir como capa de datos, integrar con cualquier proveedor
SI el usuario menciona "AWS" explícitamente → cambiar contexto a AWS y usar referencias aws-servicios.md
SI el usuario pide comparar → generar tabla comparativa entre los proveedores indicados
```

---

## Formato de Salida Requerido

Todo archivo de salida debe incluir estas secciones en orden:

1. **Encabezado** — Empresa/Proyecto, Fecha, Proveedor principal, Versión
2. **Resumen Ejecutivo** — ≤ 5 párrafos
3. **Supuestos** — Lista explícita de todo lo asumido
4. **Diagrama de Arquitectura** — Mermaid por opción
5. **Opciones Arquitectónicas** — A, B, C con pros/contras
6. **Tabla Comparativa** — criterios clave
7. **Desglose de Servicios** — tabla con servicio, SKU, costo estimado, justificación
8. **Fases de Implementación** — tabla + descripción por fase
9. **Roadmap Visual** — diagrama Gantt en Mermaid
10. **Riesgos y Mitigaciones** — tabla
11. **Recomendación Final** — opción sugerida con justificación
12. **Referencias** — links a documentación oficial
