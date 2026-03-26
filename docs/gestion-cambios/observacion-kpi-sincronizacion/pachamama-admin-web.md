# Changelog - Pachamama Admin Web

**Observación Relacionada:** KPIs e Integridad en Sincronización de Actividades.  
**Fecha:** Marzo 2026

## 1. Resumen de Cambios
El cliente web para la gestión de proyectos se realineó integralmente para dar soporte y reportar de manera visual, estructurada y responsiva todas las directrices generadas por las refabricaciones de la Sincronización Móvil. Se incluyen KPIs críticos a la vista de gestores del sistema.

## 2. Nuevas Funcionalidades y Detalle de Cambios
- **Tarjeta Dedicada de "Tasa de Éxito de Sincronización":**
  - Se incorporó formalmente en el módulo de "Resumen de Proyecto", una instancia en gráfico de Barra (*Bar Chart*) categorizando la tasa de sincronización de campo.
  - Indicadores con código semáforo: 🟢 **Exitosas**, 🔴 **Fallidas**, 🟡 **Recuperadas** (corregidas mediante reintento).
  - Incluye metacaracterísticas derivadas como la suma natural ("Total de Actividades") y los promedios calculados sobre fallas ("Promedio de Reintentos").
- **Corrección en Canvas de Gráfico circular ("Estado de Validación"):**
  - **Problema originario:** Existía un bug en el renderizado con componentes `Chart.js` (`<app-donut-chart>`). Por fallos en las asignaciones flexibles, el *canvas* se contraía perdiendo de vista visualmente todo excepto el texto numérico en el centro de la dona.
  - **Solución:** Se forzó un estilo universal de bloque responsivo resolviéndolo a través de todo el *front-end* sin desacomodar *layouts* parentales.
- **Renovación del Resumen Visual (Grid Layout):**
  - Reestructuración de la base CSS del summary; los elementos en desktop se ven en dos columnas amplias (aprovechando monitores largos) mientras que en vista de tablets y móvil el grid colapsa en una vertical natural apilable.

## 3. Cambios Técnicos y Estructurales
- **Front-end - Servicio de API:**
  - Consumo activo del nuevo Endpoint REST del API para KPIs a través de `projects.service.ts` -> `getSyncSuccessRateKpi(projectId)`.
- **Evolución del Componente `DonutChartComponent`:**
  - Inyección de pseudo-constructor host global en `shared/components/donut-chart/donut-chart.component.ts`: `:host { display: block; width: 100% }`.
- **Adaptaciones Integrales TS/UI:**
  - Modelo formal `SyncSuccessRateKpi` agregado y adaptaciones directas en `Signals`, *Computed values* y hojas de estilo SCSS sobre el controlador de página `project-detail.page`.
