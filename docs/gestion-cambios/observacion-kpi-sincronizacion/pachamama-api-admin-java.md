# Changelog - Pachamama Admin API (Java)

**Observación Relacionada:** KPIs e Integridad en Sincronización de Actividades.  
**Fecha:** Marzo 2026

## 1. Resumen de Cambios
Se dotó al Backend Administrativo (`pachamama-api-admin`) de la lógica necesaria para extraer, transformar y exponer, de forma segura, todas las métricas subyacentes recabadas por el pipeline de sincronización (`pachamama-api-sync`). Esto permite habilitar interfaces gráficas analizando la tasa de eficacia de campo.

## 2. Nuevas Funcionalidades y Detalle de Cambios
La API cuenta ahora con métricas avanzadas (KPIs operativos), entregando de forma estructurada para cada Proyecto de campo:
- **Tasa de Éxito de Sincronización:** Cálculo en porcentaje de actividades bien procesadas contra fallas.
- **Distribución de Fallas:** Análisis porcentual identificando el tipo de error más frecuente que impacte a un proyecto.
- **Volumetría de Reintentos:** Histórico de la cantidad de repeticiones realizadas (o fallidas) tratando de sacar la carga.
- **Desglose de Validaciones:** Cantidades totales entre elementos "Aprobados", "Rechazados", "Pendientes".

*Despliegue General Endpoint Clave:*
`GET /api/v1/admin/kpis/sync/by-project/{projectId}/success-rate`

## 3. Cambios Técnicos y Estructurales
- **Seguridad Restringida:** Los nuevos endpoins están estrictamente mapeados a autenticaciones perimetrales bajo el rol del gestor de proyecto (`ADMIN_EMPRESA`) respetando su pertenencia por Tenant.
- **Migraciones de Base de Datos (Flyway):**
  - `V97`: Inyección de funciones nativas Postgres para obtención de agregados (`audit.get_sync_success_rate_by_project()`, `audit.get_sync_error_distribution_by_project()`).
  - `V98`: Expansión de columnas de métricas para reintentos (`failed_attempts_total`, `retry_attempts_after_failure`, `avg_retries_per_activity`).
  - `V99`: Corrección de consistencia y mapeo paramétrico (`camelCase` a `snake_case` del `projectId`).
- **Nuevos Data Transfer Objects (DTO):**
  - Implementación de `SyncSuccessRateDto`.
  - Implementación de `SyncErrorDistributionDto`.
  - Implementación de `ActivityValidationStatusKpiDto`.
