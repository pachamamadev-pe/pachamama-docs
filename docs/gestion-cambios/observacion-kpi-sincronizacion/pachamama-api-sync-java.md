# Changelog - Pachamama API Sync (Java)

**Observación Relacionada:** KPIs e Integridad en Sincronización de Actividades.  
**Fecha:** Marzo 2026

## 1. Resumen de Cambios
El microservicio `pachamama-api-sync`, puente asíncrono desde los dispositivos móviles, incorpora mejoras severas para evitar omisiones por fallos de dependencias, registrar auditorías avanzadas (generando información para KPIs directos) y mitigar pérdidas con reprocesamiento automatizado inteligente.

## 2. Nuevas Funcionalidades y Correcciones
- **Unificación del Flujo de Procesamiento:** Anteriormente fragmentado, ahora un solo procesador maneja actividades y unidades forestales. Al crear un elemento `inventory`, el sistema crea la *Unidad Forestal* antes de registrar la actividad para evitar bloqueos por dependencias rotas.
- **Soporte para "Árboles Tocón" (`forest_is_tree_stump`):** Integración natural de la relación estricta `forest_parent_unit_id` permitiendo que el árbol tocón siempre herede las características de su planta progenitora sin generar inconsistencias.
- **Captura Universal de Errores (Trazabilidad y KPIs):** Se agregó soporte integral de diagnóstico de excepciones:
  - Consolidado en `audit.sync_errors` (PostgreSQL).
  - Snapshot de transacciones (`SUCCESS`, `SYSTEM_ERROR`, etc.) persistidas en MongoDB (`sync_message_logs`).
- **Reprocesamiento Automatizado a través de DLQ (Dead Letter Queue):** Los elementos fallidos por problemas de infraestructura entran en una *"Cola de letras muertas"*. Automáticamente un *Scheduler* repasa esta base cada 1 hora para reinyectar el trabajo, impidiendo pérdidas.
- **Detección de "Error de Origen":** Bloqueo de peticiones que ya vienen reportadas con averías en el dispositivo móvil (por medio de `error_code`/`error_message`). No se intentan guardar datos erróneos en el *Postgres Core*.

## 3. Cambios Técnicos y Estructurales
- **Infraestructura de Colas (Azure Service Bus):** Uso extenso de colas con `$DeadLetterQueue` incorporado de forma perimetral.
- **Nuevos Endpoints Explicitos (REST):**
  - **Envío manual a colas:** `POST /api/v1/messages/activity`, `POST /api/v1/messages/forest-unit`.
  - **Consulta:** `GET /api/v1/activities/search` y `/forest-units`.
- **Ecosistema de Bases de Datos:** Cobertura Dual con **PostgreSQL** para resguardo Core (`core.activities`, `core.forest_units`, `audit.sync_batches`) y **MongoDB** para telemetría ágil (`sync_message_logs`).

## 4. Diferenciación de Estados

| Estado | Significado Analítico | Ubicación del Dato |
|---|---|---|
| ✅ `SUCCESS` | Procesado y guardado correctamente | Postgres y Mongo |
| 🔵 `DUPLICATE` | Mensaje ya procesado anteriormente | Solo Mongo |
| ⚠️ `VALIDATION_ERROR` | Datos inválidos o faltantes | Auditoría Sync Errors (Pg) y Mongo |
| ❌ `SYSTEM_ERROR` | Error técnico (red, BD, inconsistencia) | Errors, Mongo y repuesto en DLQ |
| 🔴 `SOURCE_ERROR` | Error reportado y emitido por origen móvil | Errors (Pg) y Mongo |
