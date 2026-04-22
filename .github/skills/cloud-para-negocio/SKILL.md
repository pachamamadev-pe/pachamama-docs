---
name: cloud-para-negocio
description: "Skill para traducir informes técnicos de arquitectura cloud a lenguaje de negocio. Usar cuando el usuario quiera: presentar un informe de arquitectura cloud a directores o gerentes no técnicos, resumir opciones de arquitectura en términos de costo-beneficio, convertir un análisis de infraestructura en una presentación ejecutiva, explicar qué implica una decisión de cloud para el negocio, comparar opciones tecnológicas en términos de impacto, riesgo y retorno de inversión. Acepta como insumo archivos Markdown o texto de informes generados por el equipo de arquitectura. Genera un archivo Markdown con lenguaje ejecutivo como entregable."
argument-hint: "Informe técnico de arquitectura cloud, informe de costos o descripción del sistema a traducir al lenguaje de negocio"
---

# Cloud para Negocio — Traductor Ejecutivo de Arquitectura

Convierte informes técnicos de arquitectura cloud en documentos ejecutivos comprensibles para directores, gerentes y tomadores de decisión sin perfil técnico.

**Principio guía:** ningún párrafo del entregable debe requerir conocimientos de informática para ser comprendido. Si menciona un servicio técnico, explica qué *hace* para el negocio, no cómo funciona internamente.

---

## Principios de Operación

1. **Cero jerga técnica sin traducción** — todo término técnico va acompañado de su equivalente en lenguaje de negocio entre paréntesis o en un glosario al final.
2. **Foco en impacto** — el lector quiere saber: ¿cuánto cuesta?, ¿qué riesgo tiene?, ¿cuándo estará listo?, ¿qué gana el negocio?
3. **Decisión visible** — cada sección debe dejar clara la pregunta que el directivo necesita responder.
4. **Números reales sobre porcentajes vacíos** — preferir "S/ 12 000 al mes" antes que "costos optimizados".
5. **Lenguaje positivo y orientado a oportunidad** — los riesgos se enmarcan como riesgos gestionables, no como amenazas.
6. **Markdown siempre** — entregable en archivo `.md` con nomenclatura `NEGOCIO-<PROYECTO>-<YYYYMMDD>.md` en la carpeta `negocio/` del workspace.

---

## Flujo de Trabajo

### Paso 1 — Recibir y analizar el insumo técnico

El usuario puede proporcionar el insumo de las siguientes formas:

| Tipo de insumo | Acción |
|---------------|--------|
| Archivo Markdown (ej: informe `ARQ-*.md`) | Leer con `read_file` y extraer secciones clave |
| Informe de costos Azure (ej: `AZURE-COSTOS-*.md`) | Leer con `read_file` y procesar tabla de costos |
| Texto pegado directamente en el chat | Procesarlo como fuente primaria |
| Nombre de archivo sin ruta | Buscar con `file_search` en el workspace |
| Descripción verbal del sistema | Pedir al usuario que adjunte el informe o que describa más |

Extraer del informe técnico los siguientes bloques de información:

```
✔ Nombre del proyecto o sistema
✔ Proveedor cloud (Azure, AWS, GCP)
✔ Opciones de arquitectura propuestas (A, B, C si existen)
✔ Servicios técnicos utilizados (lista)
✔ Costos estimados por opción (mensual y anual)
✔ Tiempos de implementación por fase
✔ Riesgos identificados
✔ Recomendación del equipo técnico
✔ Supuestos declarados
```

Si falta algún bloque crítico (costos o tiempos), indicarlo con `[DATO PENDIENTE — solicitar al equipo técnico]`.

---

### Paso 2 — Traducción de Servicios Técnicos

Usar el diccionario de traducción para cada servicio hallado en el informe:

| Término técnico | Traducción para negocio |
|----------------|------------------------|
| Azure App Service / Kubernetes / ECS | Servidor que ejecuta la aplicación en la nube |
| Azure SQL / PostgreSQL / RDS | Base de datos de la empresa alojada en la nube |
| Azure Blob Storage / S3 | Repositorio seguro de archivos y documentos |
| Azure Functions / Lambda | Tareas automáticas que solo consumen recursos cuando se ejecutan |
| Azure IoT Hub | Canal centralizado de recepción de datos desde sensores o dispositivos |
| Azure API Management | Puerta de entrada controlada para las integraciones con terceros |
| Redis Cache | Memoria temporal que acelera las respuestas del sistema |
| Azure DevOps / CI/CD Pipeline | Proceso automatizado de despliegue de nuevas versiones sin intervención manual |
| VNet / Firewall / NSG | Red privada y sistema de seguridad perimetral |
| Azure Monitor / Application Insights | Panel de control y alertas del estado del sistema |
| SLA 99.9% | El sistema estará disponible al menos 99.9% del tiempo (máx. 8.7 h de parada al año) |
| SLA 99.5% | El sistema estará disponible al menos 99.5% del tiempo (máx. 43.8 h de parada al año) |
| AES-256 / TLS 1.3 | Cifrado de datos en tránsito y en reposo equivalente al estándar bancario |
| Árbol de Merkle / SHA-256 | Sello digital que garantiza que los registros no pueden alterarse retroactivamente |
| Multi-tenant / RLS | Cada cliente ve únicamente sus propios datos, aunque compartan infraestructura |
| Offline-first | La aplicación funciona sin internet y sincroniza cuando recupera conexión |
| DR / Disaster Recovery | Plan de contingencia para restaurar el servicio ante una falla grave |
| Microservicios | Sistema dividido en módulos independientes; si uno falla, los demás continúan |
| Serverless | Infraestructura que no cobra cuando no hay actividad |

Si el informe contiene un término técnico no listado, crearlo en el momento siguiendo el patrón: *qué hace para el negocio, no cómo funciona*.

---

### Paso 3 — Estructura del Documento Ejecutivo

Generar el informe en el siguiente orden exacto:

#### 3.1 Encabezado
```
Proyecto:       <nombre del proyecto>
Preparado por:  Equipo de Arquitectura Cloud
Fecha:          <fecha actual>
Versión:        1.0
Audiencia:      Dirección / Gerencia General
```

#### 3.2 Resumen para la Dirección (≤ 5 oraciones)
Responde en lenguaje directo: qué se propone, por qué, qué implica para el negocio y cuál es la recomendación. Este párrafo debe poder leerse en 30 segundos.

#### 3.3 ¿Qué se está construyendo?
Descripción del sistema en 3–5 párrafos sin términos técnicos. Enfocarse en:
- Qué problema de negocio resuelve
- Quiénes lo usan y cómo
- Qué beneficio tangible genera (eficiencia, cumplimiento normativo, reducción de costos, nuevos ingresos)

#### 3.4 Las Opciones Disponibles
Para cada opción arquitectónica propuesta por el equipo técnico, presentar:

```markdown
### Opción [A / B / C]: <nombre ejecutivo, no técnico>
**En una línea:** <qué es esta opción para el negocio>

| Dimensión               | Detalle                                      |
|------------------------|----------------------------------------------|
| Costo mensual estimado | S/ X,XXX / USD X,XXX                        |
| Costo anual estimado   | S/ XX,XXX / USD XX,XXX                      |
| Tiempo de puesta en marcha | X semanas / X meses                    |
| Nivel de riesgo        | Bajo / Medio / Alto                          |
| Disponibilidad del servicio | X% (equivale a máx. X horas de parada/año) |
| ¿Para qué tipo de negocio es ideal? | <descripción>              |

**Lo que el negocio gana:** <beneficios concretos>
**Lo que el negocio asume:** <compromisos o limitaciones>
```

#### 3.5 Comparación de Opciones

Tabla ejecutiva de decisión:

| Criterio de Negocio | Opción A | Opción B | Opción C |
|--------------------|----------|----------|----------|
| Inversión mensual | | | |
| Velocidad de lanzamiento | | | |
| Riesgo operativo | | | |
| Capacidad de crecimiento | | | |
| Cumplimiento normativo | | | |
| Costo de salida (vendor lock-in) | | | |
| **Puntaje ejecutivo (1–5)** | | | |

#### 3.6 ¿Qué implica para el equipo y los procesos?
Impacto organizacional: ¿requiere contratar personal?, ¿requiere capacitación?, ¿cambia algún proceso actual del negocio?

#### 3.7 Cronograma en Lenguaje de Negocio

```
Mes 1–2:   Preparación y configuración inicial
Mes 3–4:   Construcción de las funcionalidades principales
Mes 5:     Pruebas con usuarios piloto
Mes 6:     Lanzamiento al negocio completo
```
Traducir las fases técnicas del informe original. Usar meses, no sprints ni semanas técnicas.

#### 3.8 Riesgos del Negocio y Plan de Respuesta

| Riesgo | Probabilidad | Impacto en el negocio | ¿Cómo se gestiona? |
|--------|-------------|----------------------|-------------------|
| | Baja / Media / Alta | Bajo / Medio / Alto | |

Máximo 5 riesgos. Priorizados por impacto. Sin uso de términos técnicos en la descripción del riesgo.

#### 3.9 Costo Total de Propiedad (CTP)

Presentar el costo de la opción recomendada en perspectiva de 12 y 36 meses:

| Horizonte | Inversión total estimada |
|-----------|-------------------------|
| 12 meses | USD / S/ |
| 36 meses | USD / S/ |

Incluir una nota sobre qué está incluido y qué no (soporte, licencias adicionales, costo de personal, etc.).

#### 3.10 Recomendación
Cuál opción recomienda el equipo técnico y **por qué es la más conveniente para el negocio** (no técnicamente, sino en términos de valor, costo y riesgo equilibrados).

#### 3.11 Próximos Pasos y Decisiones Requeridas
Lista de acciones concretas que la Dirección debe tomar o aprobar, con fecha sugerida y responsable:

| # | Acción | Responsable | Fecha sugerida |
|---|--------|-------------|---------------|
| 1 | Aprobar opción de arquitectura | Gerencia General | |
| 2 | Aprobar presupuesto mensual | Gerencia Financiera | |
| 3 | Designar responsable del proyecto | CTO / Gerencia TI | |

#### 3.12 Glosario Ejecutivo
Listar todos los términos técnicos encontrados en el informe original con su traducción ejecutiva, ordenados alfabéticamente.

---

### Paso 4 — Reglas de Calidad del Entregable

Antes de guardar el archivo, verificar:

```
✔ ¿Todos los montos están en la moneda del informe original o en la que el usuario indicó?
✔ ¿Ningún párrafo contiene acrónimos técnicos sin explicación entre paréntesis?
✔ ¿La sección "Resumen para la Dirección" puede entenderse en 30 segundos?
✔ ¿La tabla comparativa tiene datos para todas las opciones presentadas?
✔ ¿Los riesgos están descritos en términos de impacto al negocio, no al sistema?
✔ ¿El cronograma usa meses/trimestres, no sprints ni fases técnicas?
✔ ¿La sección de próximos pasos tiene al menos 3 acciones concretas?
```

Si algún criterio falla, corregirlo antes de guardar.

---

### Paso 5 — Guardar el Entregable

- **Directorio destino**: `negocio/` en la raíz del workspace (crear si no existe).
- **Nombre del archivo**: `NEGOCIO-<PROYECTO>-<YYYYMMDD>.md`
- Confirmar al usuario la ruta del archivo generado.
- Ofrecer opción de generar también una versión en formato PPTX usando el skill `pptx`.

---

## Reglas de Comportamiento

```
SI el insumo es solo un informe de costos (sin arquitectura) →
   generar igual el documento ejecutivo, pero indicar que falta contexto funcional

SI el informe tiene más de 3 opciones →
   consolidarlas en máximo 3 (Conservadora, Equilibrada, Ambiciosa)

SI no hay costos en el informe →
   incluir [DATO PENDIENTE] e indicar cómo solicitarlo al equipo técnico

SI el usuario pide una versión para presentación PowerPoint →
   invocar el skill `pptx` con el documento generado como fuente

SI el usuario indica la moneda preferida (soles, USD, euros) →
   usar esa moneda en todo el documento; si no indica, usar la del informe original

SI el informe menciona proveedores específicos (Azure, AWS, GCP) →
   no hacer mención del proveedor por nombre en las secciones directivas;
   usar en su lugar "nuestro proveedor cloud" o "la plataforma cloud contratada",
   salvo que el usuario indique que la Dirección debe conocer el proveedor

SI el usuario proporciona el nombre de una empresa como audiencia →
   adaptar el tono del documento a esa empresa (PYME vs. Enterprise)
```

---

## Ejemplo de Apertura del Documento

```markdown
# Resumen Ejecutivo — Infraestructura Digital para [NOMBRE DEL PROYECTO]

**Preparado por:** Equipo de Arquitectura Cloud  
**Fecha:** [FECHA]  
**Para:** Dirección General / Gerencia

---

## Resumen para la Dirección

Se ha evaluado la infraestructura tecnológica necesaria para soportar [descripción funcional
del sistema en lenguaje de negocio]. El equipo técnico analizó tres alternativas con
diferentes equilibrios entre costo, velocidad de implementación y nivel de riesgo.
La opción recomendada requiere una inversión mensual de USD X,XXX y puede estar operativa
en X meses. Esta infraestructura permitirá [beneficio de negocio principal].
```

---

## Integración con Otros Skills

| Situación | Skill a invocar |
|----------|----------------|
| El usuario quiere generar el informe técnico de partida | `arquitecto-cloud` |
| El usuario quiere obtener los costos reales de Azure | `azure-pricing` |
| El usuario quiere exportar este resumen a Word | `docx` |
| El usuario quiere crear una presentación con este resumen | `pptx` |
| El usuario trabaja con el proyecto Pachamama | `build-pachamama-docs` |
