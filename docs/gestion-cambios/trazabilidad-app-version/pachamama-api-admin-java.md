# Changelog - Pachamama Admin API (Java)

**Cambio Relacionado:** Trazabilidad de Versión de App en Actividades.  
**Fecha:** Marzo 2026

## 1. Resumen de Cambios

Se actualizó el backend administrativo para exponer el campo `app_version` en los endpoints de detalle de actividad, permitiendo que la interfaz web muestre la versión de la app con la que se registró cada actividad.

## 2. Cambios Implementados

- **Exposición de `app_version` en el detalle de actividad:** El endpoint de detalle de actividad ahora retorna el campo `app_version` como parte de su respuesta, disponible para el consumo desde el frontend.

## 3. Cambios Técnicos y Estructurales

- **DTO de respuesta actualizado:** Se añadió el campo `appVersion` al DTO de detalle de actividad (`ActivityDetailDto`) con su respectivo mapeo desde la entidad.
- **Query / Repository:** La consulta que obtiene el detalle de la actividad fue actualizada para incluir el campo `app_version` de la tabla `core.activities`.
