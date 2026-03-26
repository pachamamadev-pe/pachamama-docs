# Changelog - Pachamama Mobile Android

**Versión:** 1.0.1  
**Observación Relacionada:** KPIs e Integridad en Sincronización de Actividades.  
**Fecha:** Marzo 2026

## 1. Resumen de Cambios
Este componente recibió mejoras estructurales orientadas a garantizar la robustez en la sincronización de actividades, eliminando la pérdida de evidencias multimedia (imágenes) asociadas a los formularios llenados y optimizando la gestión de errores mediante reintentos automáticos controlados.

## 2. Nuevas Funcionalidades y Correcciones
- **Validación de Integridad Multimedia:** Antes de ensamblar y enviar el payload final de la actividad, se verifica estricitamente que todos los archivos multimedia referenciados en el formulario existan y cuenten con URLs remotas válidas.
- **Manejo de Archivos "Huérfanos":** Se corrigió la lógica de la base de datos local para asegurar que las fotos capturadas temporalmente queden vinculadas firmemente a su respectiva actividad al momento de guardar el progreso en el dispositivo.
- **Política Resiliente de Reintentos:**
  - Las actividades que superan los **3 intentos fallidos** son suspendidas, excluyéndolas de los ciclos automáticos para evitar un *loop* infinito.
  - El contador de intentos (`syncRetryCount`) se incrementa para ofrecer información de su estado.
  - Se guarda rastro del mensaje de error técnico (`errorCode`, `errorMessage`, `stackTrace`).
- **Experiencia de Usuario e Indicadores UI:**
  - **Listado de Tareas:** Muestra del mensaje de error y el progreso de intentos (Ej. "2/3").
  - **Detalle de la Actividad:** Tarjeta roja prominentemente indicando el fallo y posibles acciones manuales para el usuario si se llega al límite de intentos.
  - **Feedback Visual Claro:** Uso de semáforos de estado (Rojo: Error, Ámbar: Pendiente, Verde: Enviado).

## 3. Cambios Técnicos y Estructurales
- **Base de Datos Local (Room DB):** 
  - Migración versión 8 a 9. Se incorporó la columna `activityId` explícita en la tabla de fotos. Permite vinculación directa sumada al usual `fieldKey`.
  - La entidad `ActivityEntity` ahora incluye los campos `syncRetryCount` y `lastError`.
- **Optimización en Repositorios (`ActivitiesRepository`, `PhotoRepository`):** Adición de actualizaciones masivas (Bulk Update) mediante directrices `UPDATE` para vincular fotos a las actividades, reemplazando las iteraciones ineficientes en procesos anteriores.

## 4. Códigos de Error Controlados

| Código | Descripción | Acción Recomendada |
|--------|-------------|--------------------|
| `FILE_NOT_FOUND` | La foto física no se encuentra en el dispositivo. | Recapturar la evidencia faltante. |
| `PAYLOAD_VALIDATION_ERROR` | Inconsistencia entre fotos form y URLs. | Error de validación, contactar soporte. |
| `UPLOAD_ERROR` | Fallo subiendo imagen a Azure Blob Storage. | Reintento automático por sistema. |
| `NETWORK_ERROR` | No conecta al Service Bus. | Reintento automático por sistema. |
