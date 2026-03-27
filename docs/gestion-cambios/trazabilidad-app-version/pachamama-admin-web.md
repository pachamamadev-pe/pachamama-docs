# Changelog - Pachamama Admin Web

**Cambio Relacionado:** Trazabilidad de Versión de App en Actividades.  
**Fecha:** Marzo 2026

## 1. Resumen de Cambios

Se actualizó el panel administrativo web para mostrar la versión de la app móvil (`app_version`) con la que se registró cada actividad, dentro de la vista de detalle de actividad, visible para administradores y coordinadores.

## 2. Cambios Implementados

- **Visualización de `app_version` en el detalle de actividad:** Se incorporó el campo de versión de app en la sección de información de la actividad dentro del panel administrativo.

## 3. Cambios Técnicos y Estructurales

- **Modelo de datos (TypeScript):** Se añadió el campo `appVersion: string` al modelo de detalle de actividad (`ActivityDetail`).
- **Componente de detalle:** Se actualizó el template del componente de detalle de actividad para mostrar el valor de `appVersion`.
- **Servicio de API:** No se requirieron cambios adicionales al servicio, ya que el campo es retornado por el endpoint existente de detalle de actividad actualizado en la API Admin.
