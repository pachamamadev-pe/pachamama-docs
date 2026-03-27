# Changelog - Pachamama API Sync (Java)

**Cambio Relacionado:** Trazabilidad de Versión de App en Actividades.  
**Fecha:** Marzo 2026

## 1. Resumen de Cambios

El microservicio de sincronización recibe y persiste el nuevo campo `app_version` enviado por la aplicación móvil al momento de registrar una actividad, asegurando que quede almacenado en base de datos para su consulta posterior por los servicios de administración.

## 2. Cambios Implementados

- **Recepción del campo `app_version`:** Se actualizó el modelo del mensaje / DTO de entrada para aceptar el campo `app_version` enviado desde la app móvil.
- **Persistencia en base de datos:** Se mapea el valor recibido a la columna `app_version` de la tabla de actividades al momento del procesamiento del mensaje.

## 3. Cambios Técnicos y Estructurales

- **DTO de entrada actualizado:** Se añadió el campo `app_version` al modelo que representa el payload de actividad recibido desde el Service Bus / endpoint REST.
- **Entidad y repositorio:** La entidad de actividad (`Activity`) y su repositorio (`ActivityRepository`) se actualizaron para reflejar la nueva columna.
- **Migración de base de datos:** La columna `app_version` fue añadida a la tabla `core.activities` en PostgreSQL a través del repositorio `pachamama-data-dll`.
