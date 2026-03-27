# Gestión de Cambios: Observación KPI y Sincronización

## Registro de Cambios

---

## [23 – 26 Mar 2026] KPIs y Corrección en Sincronización de Imágenes

**Autor:** Jecri Do Santos  
**Período:** 23 – 26 de Marzo 2026 *(3 días)*  
**APK generada:** `v1.0.1`

**Objetivo:** Cumplir con la observación de implementar *"KPIs para mostrar tasa de éxito y fallos y corrección de pérdida de información al sincronizar imágenes en actividades"*.

### Contexto
Durante la validación del proceso de levantamiento de actividades en campo, se detectó una necesidad crítica de:
1. **Evitar la pérdida de datos multimedia (fotografías)** tomadas en campo (con y sin conexión) que presentaban inconsistencias al intentar sincronizarse con la infraestructura en la nube.
2. **Generar métricas de visibilidad (KPIs)** para medir la efectividad, las tasas de éxito y los fallos en las sincronizaciones, dando al equipo de negocio un panorama claro de la estabilidad de la plataforma.

---

### Estrategia de Solución Integral
Para resolver esto se diseñó e implementó una actualización distribuida en los componentes del ecosistema Pachamama, estableciendo una comunicación robusta, reprocesamiento de errores y visualización en tiempo real. 

A continuación, se detalla la intervención por componente (para más detalle y flujos haz clic en cada uno):

#### 1. [Pachamama Mobile Android](pachamama-mobile-android.md) `v1.0.1`
*Encargado de la captura en campo y la retención local de datos.*
- **Correcciones Principales:** Prevención de fotos "huérfanas", actualización masiva de IDs pre-sincronización y lógica de reintentos inteligente.
- **Validación de Integridad:** Se asegura de que no se envíe el payload de actividad final hasta que todas las imágenes asociadas existan garantizadas con URLs remotas válidas (Azure).

#### 2. [Pachamama API Sync (Java)](pachamama-api-sync-java.md)
*Puente asíncrono para el procesamiento unificado.*
- **Correcciones Principales:** Procesamiento unificado de Unidades Forestales y Actividades para preservar integridad referencial.
- **Trazabilidad de Errores:** Registro persistente de errores universales (MongoDB/PostgreSQL) y envío a *Dead Letter Queue (DLQ)* para su reprocesamiento automático limitando la pérdida de datos.

#### 3. [Pachamama API Admin (Java)](pachamama-api-admin-java.md)
*Proporcionador de datos al Dashboard web para gestión y monitorización.*
- **Nuevas Funcionalidades:** Endpoints específicos para extraer la tasa de éxito de sincronización por proyecto, distribución de errores y desglose del estado de validación.
- **Adecuaciones Técnicas:** Implementación de funciones SQL para extraer los KPIs directamente desde la auditoría de bases de datos.

#### 4. [Pachamama Admin Web (Frontend)](pachamama-admin-web.md)
*Punto visual para administradores y coordinadores.*
- **Nuevas Funcionalidades:** Nuevas tarjetas y gráficas de KPI (Tasas de éxito y Status de Sincronización).
- **Correcciones Principales:** Reparación visual de los componentes de tipo *Donut Graph* y reajustes del layout responsivo para el Project Summary.

---

### Conclusión y Resultados
Con estas modificaciones combinadas, el ecosistema **garantiza que ninguna imagen se pierda** por incidencias de red gracias a validaciones estrictas y el uso de la cola de reintentos. Además, provee **métricas fiables (KPIs)** que miden el rendimiento de las sincronizaciones para tener mayor control operativo del sistema en campo.

#### Resultados Obtenidos

| Indicador | Valor |
|---|---|
| Período de implementación | 23 – 26 de Marzo 2026 |
| Duración total | 3 días |
| Imágenes validadas en pruebas | ~290 imágenes |
| Actividades involucradas | 30+ actividades |
| Errores de sincronización resueltos | Pérdida de imágenes al sincronizar |
| **Tasa de éxito alcanzada** | **100% de actividades registradas correctamente** |

La validación se realizó con un lote real de **~290 imágenes distribuidas en más de 30 actividades**, confirmando que el flujo de carga y sincronización funciona correctamente de extremo a extremo, desde la captura en el dispositivo móvil hasta el registro en el servidor.
