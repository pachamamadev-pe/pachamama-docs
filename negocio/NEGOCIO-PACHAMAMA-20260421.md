# Resumen Ejecutivo de Costos y Escalamiento Cloud para Pachamama

**Proyecto:** Pachamama SaaS  
**Preparado por:** Equipo de Arquitectura Cloud  
**Fecha:** 2026-04-21  
**Version:** 1.0  
**Audiencia:** Direccion / Gerencia General

## Resumen para la Direccion

Pachamama ya cuenta con una ruta clara para crecer en Azure sin sobredimensionar infraestructura antes de tiempo. La recomendacion es iniciar y consolidar una plataforma administrada entre 2026 y 2027, con un costo referencial de **USD 606.97 a USD 854.52 por mes** en el escenario base escalado. A partir de 2028, el propio crecimiento del negocio vuelve razonable pasar a una etapa de mayor gobierno y control, con una referencia de **USD 1,402.16 a USD 1,859.30 por mes**. La etapa de resiliencia empresarial no debe activarse desde el inicio: solo se justifica cuando el negocio necesite mayor continuidad, auditoria o compromisos formales de disponibilidad, con una referencia desde **USD 2,327.05 por mes** antes de agregar capacidades enterprise adicionales. Esto permite que la conversacion de costos deje de ser abstracta y se convierta en una decision de negocio basada en crecimiento, riesgo y margen.

## Que se esta construyendo

Se esta construyendo una ruta de crecimiento para la plataforma Pachamama en la nube, de manera que el costo de tecnologia pueda crecer con el negocio sin perder control financiero. La necesidad principal no es solo alojar el sistema en Azure, sino contar con una base que permita relacionar clientes, comunidades, recolectores y evidencia multimedia con una estructura de costos entendible.

El modelo comercial proyecta pasar de **13 clientes en 2026** a **84 clientes en 2030**, y de **7,800 recolectores** a **46,800 recolectores** en ese mismo periodo. Eso implica que el almacenamiento de archivos, la base de datos, la capacidad de procesamiento y el monitoreo creceran junto con la operacion. Por esa razon, la recomendacion no es contratar desde el inicio la infraestructura mas costosa, sino evolucionar por etapas.

El beneficio para negocio es directo: se puede aprobar una base de costo realista, identificar desde que momento conviene invertir mas en control y resiliencia, y construir una politica comercial que combine un cargo base por cliente con cargos variables por uso o retencion.

## Las Opciones Disponibles

### Opcion A: Inicio Controlado y Medible

**En una linea:** una plataforma administrada, suficiente para arrancar bien y medir el negocio antes de encarecer la operacion.

| Dimension | Detalle |
|---|---|
| Costo mensual estimado | USD 606.97 a USD 854.52 |
| Costo anual estimado | USD 7,283.59 a USD 10,254.27 |
| Tiempo de puesta en marcha | Corto plazo, 2026-2027 |
| Nivel de riesgo | Bajo |
| Disponibilidad del servicio | Alta para etapa de crecimiento inicial |
| Ideal para | Lanzamiento comercial, primeras cohortes y medicion real del uso |

**Lo que el negocio gana:**

- velocidad para operar con control de costo;
- una base clara para medir cuanto cuesta atender a cada cliente;
- menor complejidad operativa para el equipo actual.

**Lo que el negocio asume:**

- menor capacidad de resiliencia avanzada que una plataforma enterprise;
- necesidad de revisar el modelo cuando el volumen y la exigencia contractual crezcan.

### Opcion B: Escala con Gobierno

**En una linea:** una etapa intermedia para cuando crecer ya no solo exige mas capacidad, sino tambien mas control.

| Dimension | Detalle |
|---|---|
| Costo mensual estimado | USD 1,402.16 a USD 1,859.30 |
| Costo anual estimado | USD 16,825.89 a USD 22,311.57 |
| Tiempo de puesta en marcha | Etapa 2028-2029 |
| Nivel de riesgo | Medio |
| Disponibilidad del servicio | Alta con mejor control operativo |
| Ideal para | Crecimiento sostenido, mayor uso de datos y mas exigencia de gobierno |

**Lo que el negocio gana:**

- mejor control sobre integraciones, datos y crecimiento por dominios;
- una estructura mas preparada para sostener expansion comercial;
- mayor capacidad para contener fugas de costo por datos, logs y procesos.

**Lo que el negocio asume:**

- una base mensual mayor que debe estar respaldada por crecimiento real;
- mas disciplina de gestion y seguimiento operativo.

### Opcion C: Resiliencia Empresarial

**En una linea:** una plataforma para continuidad reforzada, auditoria exigente y compromisos empresariales mas altos.

| Dimension | Detalle |
|---|---|
| Costo mensual estimado | Desde USD 2,327.05 antes de extras enterprise |
| Costo anual estimado | Desde USD 27,924.56 |
| Tiempo de puesta en marcha | 2029-2030+ si el negocio lo exige |
| Nivel de riesgo | Bajo en continuidad, alto en costo si se activa antes de tiempo |
| Disponibilidad del servicio | Muy alta |
| Ideal para | Clientes o contratos con alta exigencia de continuidad, seguridad o auditoria |

**Lo que el negocio gana:**

- menor exposicion a caidas o interrupciones de alto impacto;
- mayor encaje para auditorias, continuidad y exigencias empresariales;
- base para negociar servicios premium.

**Lo que el negocio asume:**

- un costo mensual significativamente mayor;
- necesidad de justificar la inversion con ingresos, riesgo o contratos concretos.

## Comparacion de Opciones

| Criterio de Negocio | Opcion A | Opcion B | Opcion C |
|---|---|---|---|
| Inversion mensual | Baja a media | Media | Alta |
| Velocidad de lanzamiento | Alta | Media | Baja |
| Riesgo operativo | Bajo | Medio | Bajo si ya existe escala suficiente |
| Capacidad de crecimiento | Buena | Alta | Muy alta |
| Control del costo | Alto | Alto | Medio si se activa antes de tiempo |
| Encaje para continuidad y auditoria | Suficiente | Bueno | Muy alto |
| **Puntaje ejecutivo (1-5)** | **5** | **4** | **3** |

## Que implica para el equipo y los procesos

La ruta recomendada no exige saltar de inmediato a una operacion compleja. Durante 2026 y 2027, el equipo puede trabajar con una plataforma administrada y con un enfoque fuerte en medicion de costos por cliente, uso y retencion. Eso reduce la carga operativa y permite aprender con evidencia en lugar de tomar decisiones por intuicion.

Para el negocio, el cambio mas importante es que la conversacion comercial ya puede organizarse sobre dos capas: un cargo base por cliente para recuperar el piso compartido de la plataforma y un cargo variable asociado al uso real, especialmente por volumen operativo y retencion de archivos. Esta logica vuelve mas defendible el pricing y reduce el riesgo de vender por debajo del costo real.

## Cronograma en lenguaje de negocio

```text
2026: Arranque controlado
      Se consolida la base cloud, se instrumentan medidores de costo y se valida
      cuanto cuesta operar la plataforma con los primeros 13 clientes.

2027: Normalizacion y control
      Se estabiliza la operacion, se afinan reglas de retencion y se mejora la
      lectura de costo por cliente antes de escalar la plataforma.

2028: Escala con gobierno
      El crecimiento esperado de 40 clientes y 24,600 recolectores justifica una
      evolucion a una etapa con mayor control de integraciones, datos y monitoreo.

2029: Revision de resiliencia
      Se evalua si el crecimiento y el riesgo operativo ya requieren componentes
      selectivos de una plataforma de mayor continuidad.

2030: Decision empresarial de continuidad
      Solo si hay exigencias contractuales, regulatorias o de continuidad, se
      activa una etapa de resiliencia reforzada con mayor costo base.
```

## Riesgos del negocio y plan de respuesta

| Riesgo | Probabilidad | Impacto en el negocio | Como se gestiona |
|---|---|---|---|
| Vender planes sin recuperar el costo real de operacion y retencion | Media | Alto | Definir pricing con cargo base y banda variable por uso/retencion |
| Activar infraestructura empresarial antes de que el mercado la pague | Media | Alto | Mantener Opcion C como decision condicionada por contratos, SLA o riesgo |
| Subestimar el peso economico de fotos, videos y retencion historica | Alta | Alto | Gobernar lifecycle, retencion y tiers de almacenamiento desde el inicio |
| Crecer en clientes sin ajustar gobierno de datos y monitoreo | Media | Medio | Usar 2028 como hito formal de paso a Opcion B |
| Tomar decisiones de inversion con medicion insuficiente | Media | Medio | Instrumentar telemetria por cliente, recolector, actividad y archivo desde la etapa inicial |

## Costo Total de Propiedad (CTP)

La lectura recomendada para negocio es usar como base el **escenario base con plataforma escalada**, porque es el que mejor refleja una operacion realista sin asumir aun componentes enterprise completos.

| Horizonte | Inversion total estimada |
|---|---|
| 12 meses | USD 7,283.59 |
| 36 meses | USD 34,363.75 |

> Incluye infraestructura cloud base estimada en el escenario recomendado y su crecimiento proyectado hasta 2028.
>
> No incluye soporte premium del proveedor, servicios profesionales, costo del equipo interno, impuestos, integraciones externas vigentes ni capas enterprise adicionales de la Opcion C.

## Recomendacion

La recomendacion para negocio es **aprobar Opcion A como base 2026-2027**, con la condicion explicita de que el proyecto llegue preparado para revisar formalmente el salto a **Opcion B en 2028**. Este enfoque equilibra valor, velocidad y prudencia financiera: permite crecer sin sobregastar desde el inicio y sin quedar atrapados en una plataforma demasiado liviana cuando el negocio ya haya escalado.

La **Opcion C** debe tratarse como una inversion selectiva en continuidad y riesgo. No es la opcion inicial recomendada porque podria consumir margen sin aportar valor equivalente durante la etapa temprana. Si el negocio logra contratos con mayores exigencias de disponibilidad, auditoria o continuidad, entonces esa inversion se vuelve defendible y comercialmente util.

## Proximos pasos y decisiones requeridas

| # | Accion | Responsable | Fecha sugerida |
|---|---|---|---|
| 1 | Aprobar Opcion A como base 2026-2027 | Direccion / Gerencia General | Abril 2026 |
| 2 | Validar politica comercial de cargo base + cargo variable | Gerencia General / Finanzas | Abril 2026 |
| 3 | Definir metricas obligatorias por cliente, recolector, actividad y archivo | Producto / TI | Mayo 2026 |
| 4 | Aprobar 2028 como hito formal de revision para evolucion a Opcion B | Direccion / TI | Mayo 2026 |
| 5 | Mantener Opcion C como decision sujeta a contratos, SLA o cumplimiento | Direccion / Comercial | Revision anual |

## Glosario ejecutivo

| Termino | Traduccion de negocio |
|---|---|
| Blob Storage | Repositorio seguro de archivos, fotos y videos |
| Observabilidad | Panel de control que muestra uso, errores y salud del sistema |
| Opcion A | Plataforma administrada de arranque controlado |
| Opcion B | Plataforma de crecimiento con mayor control |
| Opcion C | Plataforma de continuidad y resiliencia empresarial |
| PostgreSQL | Base de datos principal de la operacion |
| Retencion | Tiempo durante el cual la informacion se conserva disponible |
| SLA | Compromiso formal de disponibilidad del servicio |