# Brief de Arquitectura y Proyeccion de Costos Azure para Pachamama

**Proyecto:** Pachamama SaaS  
**Fecha:** 2026-04-21  
**Proveedor principal:** Azure  
**Version:** 0.3 - Documento base alineado con bandas de costo y hitos 2026-2030

## Resumen Ejecutivo

Este documento organiza y lleva a limpio el requerimiento de negocio para estimar la arquitectura objetivo en Azure y construir un modelo de costos que tenga coherencia con el crecimiento comercial del producto.

La necesidad central no es solo conocer cuanto costara migrar o ejecutar la plataforma, sino entender que porciones del costo son fijas, cuales crecen con el negocio y cuales dependen directamente del uso de la solucion. El objetivo final es que negocio pueda traducir esas lineas de costo en una logica de suscripcion por cliente.

El analisis debe partir de tres realidades. Primero, Pachamama hoy opera sobre una arquitectura MVP distribuida en varios proveedores y la migracion base a Azure ya fue planteada como un paso inicial. Segundo, el producto todavia no cuenta con suficiente historia operativa para proyectar crecimiento real con precision estadistica. Tercero, ya existe una senal tecnica util: el patron actual de datos permite identificar cuales entidades y flujos son los principales generadores de almacenamiento, procesamiento y retencion.

Este brief deja claro el problema, el alcance del informe esperado, los supuestos iniciales, las preguntas que el negocio necesita responder y las decisiones de arquitectura que deberan compararse en la siguiente iteracion.

Desde esta revision, el brief tambien adopta el mismo lenguaje economico que el documento de arquitectura y el anexo de costos. En particular, la discusion sobre evolucion de plataforma ya no se apoya solo en volumen proyectado, sino tambien en **bandas de costo total base en escenario escalado** para 2026-2030.

## Intencion del Documento

Este archivo servira como insumo para elaborar una version posterior del informe de arquitectura y costos Azure con mayor nivel de detalle, incluyendo diagramas, escenarios de crecimiento y una recomendacion de arquitectura base frente a una arquitectura robusta.

## Contexto de Negocio y Motivo de Migracion

Pachamama necesita proyectar el costo de su infraestructura cloud para definir precios de suscripcion sostenibles por cliente.

El producto opera bajo una logica donde:

- cada cliente gestiona una o varias comunidades;
- cada comunidad agrupa un conjunto de recolectores;
- la actividad de esos recolectores genera datos operativos, geoespaciales, trazabilidad, lotes de produccion y archivos multimedia.

Ese crecimiento del negocio impacta de forma directa la infraestructura, principalmente en:

- base de datos transaccional y geoespacial;
- almacenamiento de archivos en Blob Storage;
- procesamiento de sincronizacion y trazabilidad;
- observabilidad, retencion y replicas.

La migracion a Azure no debe evaluarse solo como una mudanza tecnica desde el estado actual, sino como una oportunidad para:

- consolidar gobierno tecnico y financiero;
- unificar monitoreo, seguridad y politicas de continuidad;
- definir una ruta clara desde un esquema MVP hasta una plataforma preparada para escalar.

## Objetivo General

Definir un marco de analisis para estimar los costos Azure de Pachamama y relacionarlos con las variables reales del negocio, de modo que se pueda construir un esquema de suscripcion por cliente con respaldo tecnico y financiero.

## Objetivos Especificos

- Identificar que recursos de Azure tienen costo base relativamente fijo.
- Identificar que recursos crecen conforme aumenta el numero de clientes, comunidades, recolectores y actividad operativa.
- Identificar que costos dependen principalmente del uso, transacciones, almacenamiento consumido o trafico.
- Comparar una arquitectura base de migracion con una arquitectura mas robusta para una etapa madura del producto.
- Evaluar el impacto de politicas de retencion de 5 y 7 anios sobre base de datos, backups y almacenamiento.
- Definir lineamientos de replicacion y continuidad para base de datos y almacenamiento.
- Establecer desde cuando sera posible reemplazar supuestos por patrones reales de crecimiento.

## Preguntas de Negocio que el Informe Debe Responder

1. Que lineas del costo Azure son fijas, semi-fijas o variables.
2. Que costos pueden asociarse directamente a cada cliente o cohorte de clientes.
3. Que variables del negocio explican mejor el aumento de costo: clientes, comunidades, recolectores, actividades, archivos, consultas, sincronizaciones o reportes.
4. Cuanto cambia el costo al pasar de una migracion base a una arquitectura mas robusta.
5. En que punto conviene evolucionar desde una arquitectura administrada simple hacia componentes mas robustos como AKS, balanceadores dedicados, replica de base de datos o mayor capacidad de red.
6. Como impactan las politicas de retencion de 5 o 7 anios sobre almacenamiento activo, almacenamiento frio, backups y recuperacion.
7. Cuando existira suficiente evidencia operativa para estimar crecimiento real en lugar de trabajar solo con escenarios.

## Mensaje Clave de Negocio

> Nos gustaria saber que lineas de la estructura de costos estan amarradas a componentes variables que puedan conectarse con las proyecciones adjuntas y tener coherencia entre los ingresos y sus correspondientes costos.

## Alcance del Estudio Esperado

El informe posterior que parta de este brief debera incluir como minimo:

- arquitectura base propuesta para migracion inicial a Azure;
- arquitectura robusta objetivo para una etapa prudente de crecimiento;
- clasificacion de costos por naturaleza: fija, escalable y por uso;
- modelo de drivers de costo vinculados a drivers de negocio;
- escenarios de crecimiento conservador, medio y agresivo;
- analisis de retencion, backups, replicacion y continuidad;
- recomendacion ejecutiva sobre cuando conviene evolucionar de una opcion a otra.

## Supuestos Iniciales de Modelado

Mientras no se consoliden metricas historicas de produccion, el analisis debera operar con supuestos explicitamente declarados.

Supuestos iniciales propuestos:

- cada cliente consume espacio de base de datos y almacenamiento de archivos de forma incremental;
- el numero de comunidades y recolectores por cliente explica una parte importante del crecimiento de datos;
- las actividades de campo son el principal generador de registros operativos y evidencia multimedia;
- como supuesto operativo inicial, un recolector puede registrar entre 10 y 200 actividades por cliente;
- cada actividad puede generar entre 1 y 20 imagenes de menos de 1 MB cada una y entre 1 y 5 videos de menos de 2 MB cada uno, almacenados en Azure Blob Storage;
- la multimedia por actividad puede crecer mas rapido que la base de datos relacional;
- la necesidad de trazabilidad y auditoria puede incrementar significativamente el costo de almacenamiento retenido en el tiempo;
- la arquitectura robusta no debe activarse desde el dia uno, sino cuando las cargas y el riesgo operativo lo justifiquen.

## Variables del Negocio que Deben Conectar Ingresos y Costos

Para que el modelo de suscripcion tenga coherencia con la infraestructura, los siguientes drivers de negocio deben quedar conectados a drivers tecnicos:

| Driver de negocio | Driver tecnico asociado | Impacto esperado |
|---|---|---|
| Numero de clientes | Aislamiento logico, consumo de BD, storage y soporte | Crecimiento transversal en casi todos los componentes |
| Comunidades por cliente | Volumen de entidades, operaciones y reportes | Aumento de datos relacionales y consultas |
| Recolectores por comunidad | Sincronizacion, autenticacion, actividad movil | Mas concurrencia, trafico y operaciones |
| Actividades por recolector | Inserciones, geodatos, trazabilidad, auditoria | Principal driver de crecimiento de BD |
| Archivos por actividad | Blob Storage (imagenes y videos), replicas, lifecycle, egress | Principal driver de almacenamiento y retencion |
| Reportes y trazabilidad | Lecturas, colas/eventos, read models | Incremento de procesamiento y observabilidad |

### Proyecciones de Negocio Incorporadas (Cierre Anual)

El Excel de negocio ya aporta una curva de crecimiento al cierre de cada anio entre 2026 y 2030. Esa curva reemplaza la ausencia previa de proyecciones y pasa a ser la base de planeamiento para el informe posterior.

| Anio | Clientes | Comunidades | Recolectores | Lotes activos | Comunidades / cliente | Recolectores / comunidad |
|---|---|---|---|---|---|---|
| 2026 | 13 | 260 | 7,800 | 17,424 | 20.00 | 30.00 |
| 2027 | 23 | 500 | 15,000 | 45,504 | 21.74 | 30.00 |
| 2028 | 40 | 820 | 24,600 | 74,964 | 20.50 | 30.00 |
| 2029 | 61 | 1,180 | 35,400 | 106,392 | 19.34 | 30.00 |
| 2030 | 84 | 1,560 | 46,800 | 138,384 | 18.57 | 30.00 |

Lecturas iniciales de la proyeccion:

- el modelo comercial mantiene una relacion muy estable de **30 recolectores por comunidad**;
- el numero de comunidades por cliente se mueve aproximadamente entre **18.6 y 21.7**;
- los lotes activos muestran una trayectoria creciente que refuerza la necesidad de modelar almacenamiento, trazabilidad y retencion desde el inicio.

### Bandas de Costo de Referencia Alineadas con Arquitectura

Para que el brief, la arquitectura formal y el anexo economico hablen exactamente el mismo lenguaje, se adopta como referencia el **escenario base con plataforma escalada**.

| Anio | Clientes | Recolectores | Lotes activos | Costo mensual base escalado | Banda recomendada |
|---|---|---|---|---|---|
| 2026 | 13 | 7,800 | 17,424 | USD 606.97 | Opcion A |
| 2027 | 23 | 15,000 | 45,504 | USD 854.52 | Opcion A |
| 2028 | 40 | 24,600 | 74,964 | USD 1,402.16 | Opcion B |
| 2029 | 61 | 35,400 | 106,392 | USD 1,859.30 | Opcion B con evaluacion selectiva de componentes C |
| 2030 | 84 | 46,800 | 138,384 | USD 2,327.05 | Opcion C solo si SLA, compliance o riesgo lo justifican |

Lectura de negocio compartida entre los tres documentos:

- **Opcion A** cubre el tramo 2026-2027 mientras el costo total base se mantiene en una banda de hasta aproximadamente **USD 855/mes**;
- **Opcion B** se convierte en referencia natural desde 2028, cuando el escenario base escalado supera aproximadamente **USD 1,400/mes** y exige mejor gobierno de APIs, datos y observabilidad;
- **Opcion C** no debe activarse por intuicion, sino cuando el negocio necesite una capa adicional de resiliencia y el costo/riesgo justifique una banda desde aproximadamente **USD 2,300/mes** antes de sumar componentes enterprise.

> Esta banda de costo no representa precio comercial final al cliente. Representa el umbral economico de infraestructura compartida sobre el que luego debe construirse margen, soporte, continuidad y pricing diferencial.

### Supuesto Operativo Cuantificado para Blob Storage

Para el modelado inicial de almacenamiento multimedia se incorpora el siguiente marco de referencia:

- un recolector puede registrar entre 10 y 200 actividades por cliente;
- cada actividad puede registrar entre 1 y 20 imagenes de menos de 1 MB cada una;
- cada actividad puede registrar entre 1 y 5 videos de menos de 2 MB cada uno;
- toda esta evidencia multimedia se almacena en Azure Blob Storage.

Aplicado sobre la proyeccion de negocio, este supuesto impacta sobre una base que pasa de **7,800 recolectores proyectados en 2026** a **46,800 recolectores proyectados en 2030**.

Como lectura preliminar para estimacion, este supuesto define un techo teorico cercano a **30 MB por actividad** en evidencia multimedia y hasta **6,000 MB por recolector/cliente** en un escenario de maxima carga, sin considerar replicas, versionado, metadatos ni politicas de retencion.

## Clasificacion Preliminar de Costos Azure

La siguiente clasificacion es inicial y debera refinarse cuando se definan los SKUs y la arquitectura final.

| Componente Azure | Naturaleza del costo | Driver principal | Comentario de negocio |
|---|---|---|---|
| Compute administrado para APIs | Semi-fijo con escalamiento | usuarios activos, concurrencia, picos | Tiene costo base y puede subir por capacidad |
| Azure Functions / procesos event-driven | Por uso o semi-fijo segun plan | ejecuciones, memoria, tiempo de proceso | Bueno para cargas intermitentes |
| Azure Database for PostgreSQL | Semi-fijo + variable por storage/backups | volumen de datos, IOPS, replicas, retencion | Uno de los costos mas sensibles del modelo |
| Azure Blob Storage | Variable por GB + operaciones + replica | archivos, tamano promedio, retencion, descargas | Debe vincularse a actividades multimedia |
| Service Bus / mensajeria | Variable o semi-fijo segun SKU | mensajes, colas, throughput | Acompania sincronizacion y eventos |
| Redis / cache | Semi-fijo | tasa de consulta y latencia requerida | Mas relacionado a performance que a retencion |
| Log Analytics / Application Insights | Variable por ingestion y retencion | volumen de logs, errores, trazas | Puede crecer rapido si no se gobierna |
| Networking, balanceadores e IPs | Mixto | trafico, exposicion publica, topologia | Relevante al madurar a arquitecturas robustas |
| Backup, replica y DR | Semi-fijo + variable por datos | tamano total, ventana de retencion, RPO/RTO | Costo obligado si se exige continuidad formal |
| AKS y componentes asociados | Costo base mas alto y escalable | nodos, trafico, alta disponibilidad | No conviene activarlo sin una justificacion clara |

## Opciones de Arquitectura a Comparar en la Siguiente Iteracion

### Opcion A - Base administrada de migracion

Arquitectura orientada a reducir complejidad operativa, usando principalmente servicios administrados y capacidades suficientes para una etapa inicial de crecimiento.

**Uso esperado:** validacion comercial, primeras cohortes de clientes, control de costos y velocidad de salida.

### Opcion B - Escalable intermedia

Arquitectura con mayor elasticidad, desacoplamiento y observabilidad, pensada para una etapa donde la sincronizacion, la trazabilidad y la multimedia aumentan de forma sostenida.

**Uso esperado:** crecimiento sostenido, necesidad de mejores SLOs y mayor gobierno tecnico.

### Opcion C - Robusta / crecimiento maduro

Arquitectura orientada a alta disponibilidad, mayor aislamiento, replicas, balanceo dedicado y eventualmente orquestacion con AKS si la carga, el throughput y la criticidad del negocio lo justifican.

**Uso esperado:** etapa madura del producto, mayor criticidad operativa y necesidad de continuidad reforzada.

## Impacto Esperado de la Migracion en Costos

El cambio hacia Azure puede generar dos efectos simultaneos:

- **Mayor costo base visible** si se pasa de una arquitectura muy fragmentada o economica de MVP hacia servicios con mayor gobierno, soporte, seguridad y resiliencia.
- **Mayor control del costo total** al centralizar monitoreo, politicas, retencion, seguridad, continuidad y escalamiento bajo una estrategia unificada.

La comparacion economica no debe hacerse solo por valor mensual bruto, sino por:

- costo por cliente atendido;
- costo por actividad procesada;
- costo por GB almacenado y retenido;
- costo por nivel de disponibilidad y riesgo mitigado.

## Retencion, Replicacion y Continuidad

Las decisiones de retencion y replicacion deben modelarse como parte estructural del costo, no como un adicional de ultimo momento.

### Retencion de datos

El negocio desea evaluar escenarios de retencion minima de 5 y 7 anios. Eso obliga a distinguir entre:

- datos calientes de operacion diaria;
- datos historicos de consulta ocasional;
- evidencias multimedia con bajo acceso pero alto valor de auditoria;
- logs y trazas tecnicas con politicas de limpieza diferentes a los datos funcionales.

### Replicacion recomendada para analisis

- **Base de datos:** evaluar alta disponibilidad zonal, read replicas si la lectura crece y politicas de backup alineadas a RPO/RTO.
- **Storage:** comparar LRS, ZRS y GRS/RA-GRS segun criticidad, costo y requerimientos de continuidad.

La mejor opcion no sera universal; dependera del nivel de riesgo aceptado, del costo por cliente objetivo y del valor de la informacion retenida.

## Momento en que Podra Estimarse el Crecimiento Real

Hoy ya existe una proyeccion comercial 2026-2030 entregada por negocio, pero aun no existe suficiente historia operativa para convertir esa curva en comportamiento real con alta confianza. Por eso, la siguiente fase debe contrastar esa proyeccion con telemetria y dejar trazados los medidores que luego permitiran recalibrar el modelo.

En terminos practicos, se recomienda considerar que habra una primera base razonable para estimacion real cuando se cumplan al menos una o varias de estas condiciones:

- entre 8 y 12 semanas de operacion con clientes reales y telemetria confiable;
- al menos 3 ciclos mensuales de facturacion y uso;
- visibilidad del promedio y percentiles de actividades por recolector;
- visibilidad del tamano promedio y frecuencia de archivos multimedia;
- visibilidad del crecimiento mensual de tablas, blobs, logs y backups.

## Datos Base Disponibles al 2026-04-21

### Snapshot STG de base de datos

El entorno de prueba reporta un total aproximado de **43 MB** de base de datos, incluyendo indices, PostGIS y objetos auxiliares.

Resumen de ocupacion por empresa:

| Empresa | Filas totales | Tablas activas | Total MB |
|---|---|---|---|
| Empresa Demo Pachamama S.A.C. | 1,895 | 11 | 5.19 MB |
| REORI CORP S.A.C. | 330 | 11 | 2.35 MB |
| COMUNIDAD CAMPESINA DE PARA | 65 | 9 | 0.75 MB |
| Empresa Demo 03 | 161 | 10 | 0.69 MB |
| DEMO 01 | 3 | 1 | 0.01 MB |
| Total BD real | - | - | 43 MB |

### Hallazgos tecnicos relevantes del snapshot

- `core.activities` y `core.forest_units` ya aparecen como tablas naturales de crecimiento operativo.
- `geo.*` y objetos PostGIS deben considerarse dentro del costo real de crecimiento, no solo las tablas de negocio visibles.
- `audit.sync_errors` presenta pocos registros pero alto peso por campos grandes; esto sugiere que la observabilidad y retencion de payloads pueden distorsionar el costo si no se gobiernan.
- `core.collection_requests` muestra mas peso relativo en indices que en datos; esto invita a revisar si la estructura actual esta sobredimensionada para el volumen presente.

### Lectura arquitectonica del dato actual

El tamanio actual es util como referencia tecnica de partida, pero todavia no representa una muestra suficiente para proyectar el crecimiento del negocio. Sirve mejor para:

- identificar las entidades con mayor potencial de crecimiento;
- reconocer patrones de almacenamiento no obvios;
- definir las metricas que si deben medirse desde el inicio en produccion.

## Informacion Adicional que Debe Recolectarse

Para que la siguiente version del informe sea financieramente util, faltan los siguientes insumos:

- confirmacion de que los valores anuales del Excel representan cierre de anio y no promedio del anio, para evitar errores de lectura financiera;
- distribucion real de actividades por recolector por dia, semana y mes, tomando como supuesto inicial un rango de 10 a 200 actividades por cliente;
- distribucion real de archivos por actividad y tamano efectivo por tipo de archivo, tomando como referencia inicial entre 1 y 20 imagenes de menos de 1 MB y entre 1 y 5 videos de menos de 2 MB, todos en Blob Storage;
- requerimientos de concurrencia, picos de uso y ventanas de sincronizacion;
- objetivos de disponibilidad, RPO y RTO;
- politicas esperadas de retencion funcional, legal y tecnica;
- supuestos de crecimiento del modulo de reportes, trazabilidad y notificaciones;
- correlacion esperada entre lotes activos, volumen documental y trazabilidad historica por cliente.

## Recomendaciones Iniciales para la Siguiente Iteracion

1. Construir el modelo de costos sobre drivers operativos, no solo sobre recursos Azure aislados.
2. Separar claramente costo de operacion diaria, costo de crecimiento y costo de continuidad.
3. Incluir tres escenarios de negocio: conservador, esperado y exigente.
4. Modelar por separado base de datos, blobs, observabilidad y replicas, porque no crecen al mismo ritmo.
5. Definir desde el inicio politicas de lifecycle y limpieza para archivos, logs y errores tecnicos voluminosos.
6. Evitar activar componentes de alta complejidad como AKS antes de que existan indicadores claros de necesidad.

## Paquete Minimo para Presentacion a Negocio

Con esta revision, ya existe un paquete coherente de tres piezas para presentar a negocio sin cambiar de lenguaje entre documentos:

| Documento | Rol en la presentacion | Mensaje principal |
|---|---|---|
| `ARQ-PACHAMAMA-AZURE-PROYECCION-COSTOS-20260421.md` | Brief base | explica el problema de negocio, los supuestos y las bandas de referencia 2026-2030 |
| `ARQ-PACHAMAMA-AZURE-ESCALAMIENTO-Y-PRICING-20260421.md` | Documento de arquitectura | muestra las opciones A/B/C, los hitos y la recomendacion tecnica alineada a costos |
| `AZURE-COSTOS-PACHAMAMA-DRIVERS-20260421.md` | Anexo economico | demuestra las formulas, tablas anuales y drivers que sostienen la conversacion financiera |

Decisiones que negocio ya puede tomar con este paquete:

1. Aceptar **Opcion A** como base 2026-2027 y usarla como punto de partida presupuestal.
2. Reconocer **2028** como el primer punto formal de evaluacion para evolucionar a **Opcion B**.
3. Tratar **Opcion C** como una decision de resiliencia y riesgo, no como una inversion obligatoria desde el inicio.
4. Diseñar el pricing comercial con un **cargo base + cargo variable por consumo/retencion**, en lugar de una tarifa plana sin trazabilidad economica.

## Entregables Esperados de la Proxima Version

- diagrama Mermaid de arquitectura base propuesta;
- diagrama Mermaid de arquitectura robusta propuesta;
- tabla de costos clasificada por fijo, escalable y por uso;
- mapeo entre drivers de negocio y drivers tecnicos;
- comparacion de impacto economico entre arquitectura base y robusta;
- recomendacion ejecutiva para pricing de suscripcion y evolucion de infraestructura.

## Referencias

- Arquitectura MVP vigente: [../MVP-ARCHITECTURE.md](../MVP-ARCHITECTURE.md)
- Inventario Azure actual: [../infrastructure/azure.md](../infrastructure/azure.md)
- Documento formal de migracion Azure: [ARQ-PACHAMAMA-AZURE-FULL-20260410-v2.md](ARQ-PACHAMAMA-AZURE-FULL-20260410-v2.md)