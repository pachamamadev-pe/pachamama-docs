# Changelog - Pachamama Mobile Android

**Versión:** 1.0.2  
**Cambio Relacionado:** Trazabilidad de Versión de App en Actividades.  
**Fecha:** Marzo 2026

## 1. Resumen de Cambios

Se actualizó la aplicación móvil para incluir la versión de la app (`app_version`) en el payload enviado durante la sincronización de actividades, permitiendo al backend registrar con qué versión fue capturada cada actividad.

## 2. Cambios Implementados

- **Envío de `app_version` en sincronización:** Se incluye el valor de la versión actual de la app (obtenido de `BuildConfig.VERSION_NAME`) en el objeto de sincronización de actividades enviado al API Sync.

## 3. Cambios Técnicos y Estructurales

- **Modelo de datos de sincronización:** Se añadió el campo `app_version: String` al DTO / payload de actividad enviado al API Sync.
- **Obtención dinámica del valor:** Se utiliza `BuildConfig.VERSION_NAME` para asegurar que el valor siempre refleje la versión instalada en el dispositivo.
- **Migración de BD local (Room DB):** No se requirió migración ya que el campo es parte del payload de red, no de entidades locales persistidas.

## 4. Versiones

| Campo | Valor |
|---|---|
| Versión anterior | `1.0.1` |
| Versión actual | `1.0.2` |
| Tipo de cambio | Funcionalidad nueva |
