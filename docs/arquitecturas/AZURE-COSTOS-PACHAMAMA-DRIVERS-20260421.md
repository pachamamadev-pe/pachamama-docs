# Anexo de Costos Azure y Drivers de Negocio para Pachamama SaaS

**Proyecto:** Pachamama SaaS  
**Fecha:** 2026-04-21  
**Region principal asumida:** Brazil South  
**Moneda:** USD  
**Version:** 1.1  
**Documento relacionado:** [ARQ-PACHAMAMA-AZURE-ESCALAMIENTO-Y-PRICING-20260421.md](ARQ-PACHAMAMA-AZURE-ESCALAMIENTO-Y-PRICING-20260421.md)

## Resumen Ejecutivo

Este anexo traduce la arquitectura propuesta a una estructura economica util para negocio. El foco no esta en entregar una unica cifra mensual cerrada, sino en usar la proyeccion comercial 2026-2030 ya disponible para identificar **que lineas del costo Azure dependen del crecimiento comercial** y como deben leerse para que el precio de suscripcion conserve coherencia con el costo de atender a cada cliente.

La conclusion principal es que el costo Azure debe separarse en tres capas:

- **Costo fijo o piso operativo:** recursos necesarios para que la plataforma exista aunque el trafico sea bajo.
- **Costo escalable:** recursos cuyo piso existe, pero crecen conforme sube la capacidad o el volumen retenido.
- **Costo por uso:** recursos que aumentan directamente con actividades, archivos, mensajes, lecturas, escrituras o ingestion de logs.

Con la informacion actualmente disponible, el driver variable mas facil de conectar a negocio es la **evidencia multimedia en Blob Storage**. Sin embargo, a medida que el producto madure, los costos mas sensibles no seran solo los GB nuevos del mes, sino la **retencion acumulada**, las **replicas** y la **observabilidad**. Por eso, el pricing de clientes no debe construirse solo con un cargo fijo, sino con una combinacion de piso base mas consumo explicable por driver.

## Supuestos del Modelo

- El Excel de negocio aporta una proyeccion de cierre anual 2026-2030 para clientes, comunidades, recolectores y lotes activos.
- El rango informado de 10 a 200 actividades por recolector por cliente se usa como unidad base del modelo.
- Para transformar el modelo a costo mensual, se asume inicialmente que ese rango corresponde a un periodo mensual hasta que negocio confirme otra cadencia.
- Cada actividad puede generar entre 1 y 20 imagenes de menos de 1 MB y entre 1 y 5 videos de menos de 2 MB.
- Toda la evidencia multimedia se almacena en Azure Blob Storage.
- Los precios listados abajo provienen de consultas recientes a Azure Retail Prices API cuando esa API ofrecio datos del servicio. Donde la API no retorno resultados, se indica explicitamente que debe validarse en calculadora oficial.

## Proyecciones de Negocio Incorporadas (2026-2030)

| Anio | Clientes | Comunidades | Recolectores | Lotes activos | Comunidades / cliente | Recolectores / comunidad | Lotes activos / recolector |
|---|---|---|---|---|---|---|---|
| 2026 | 13 | 260 | 7,800 | 17,424 | 20.00 | 30.00 | 2.23 |
| 2027 | 23 | 500 | 15,000 | 45,504 | 21.74 | 30.00 | 3.03 |
| 2028 | 40 | 820 | 24,600 | 74,964 | 20.50 | 30.00 | 3.05 |
| 2029 | 61 | 1,180 | 35,400 | 106,392 | 19.34 | 30.00 | 3.01 |
| 2030 | 84 | 1,560 | 46,800 | 138,384 | 18.57 | 30.00 | 2.96 |

Lectura estructural:

- la proyeccion sostiene **30 recolectores por comunidad** de forma constante;
- el crecimiento de clientes viene acompanado por un incremento muy fuerte del parque operativo total;
- el numero de lotes activos casi se multiplica por 8 entre 2026 y 2030, lo que refuerza el peso de trazabilidad, historial y evidencia multimedia.

## Lineas de Costo y Naturaleza Economica

| Linea de costo | Naturaleza | Precio de referencia | Unidad | Conexion con negocio | Estado |
|---|---|---|---|---|---|
| PostgreSQL Flexible Server - compute base | Semi-fijo | `0.1532 USD/h` para `2 vCore` | Hora | Piso de operacion del core transaccional | Confirmado via API |
| Blob Storage Hot LRS | Variable | `0.0489 USD/GB/mes` | GB/mes | Directamente ligado a imagenes, videos y retencion | Confirmado via API |
| Blob Storage operations | Variable | `0.00728 USD/10K ops` | 10K operaciones | Sube con uploads, lecturas y lifecycle | Confirmado via API |
| Service Bus Standard base | Fijo | `10 USD/mes` | Mes | Piso de asincronia y eventos | Confirmado via API |
| Container Apps - vCPU activa | Semi-fijo + uso | `0.000024 USD/s` | vCPU-segundo | Sube con trafico, concurrencia y ventanas de sincronizacion | Confirmado via API |
| Container Apps - memoria activa | Semi-fijo + uso | `0.000003 USD/GiB-s` | GiB-segundo | Sube con permanencia y volumen de trabajo | Confirmado via API |
| Container Apps - requests | Variable | `0.4 USD/1M requests` | 1 millon de requests | Directamente ligado a uso de APIs | Confirmado via API |
| Application Gateway WAF | Fijo + capacidad | `0.4 USD/h` fijo + `0.008 USD/h` por capacidad | Hora | Solo aplica si negocio necesita perimetro enterprise | Confirmado via API |
| AKS Standard + Uptime SLA | Fijo alto | `0.6 USD/h` + `0.1 USD/h` | Hora | Solo se justifica con mayor criticidad o escala | Confirmado via API |
| Service Bus Premium | Fijo alto | `0.9275 USD/h` por Messaging Unit | Hora | Aislacion y resiliencia avanzadas | Confirmado via API |
| Redis | Semi-fijo | Precio no disponible via API | Mes | Mejora performance, pero no suele ser el principal driver comercial | Validar en calculadora |
| App Insights / Log Analytics | Variable | Precio no consolidado en esta iteracion | Ingestion y retencion | Se conecta con trafico, errores y verbosidad tecnica | Validar en calculadora |

## Formula de Blob Storage

Para efectos de negocio, la formula mas importante es la del almacenamiento multimedia.

```text
Blob_GB_periodo =
  Recolectores
  x Frecuencia
  x Actividades_por_recolector
  x ((Imagenes_por_actividad x 1 MB) + (Videos_por_actividad x 2 MB))
  / 1024
```

```text
Costo_Blob_Hot_USD = Blob_GB_periodo x 0.0489
```

Donde:

- `Frecuencia = 1` si el rango 10-200 ya corresponde a un mes.
- `Frecuencia = 4.3` si el rango corresponde a una semana.
- `Frecuencia = 30` si el rango corresponde a un dia.

## Escenarios de Multimedia por Recolector

Los siguientes escenarios usan la unidad de observacion base definida en este anexo. Sirven para que negocio conecte rapidamente recolectores y evidencia con crecimiento de Blob Storage.

| Escenario | Actividades | Imagenes / actividad | Videos / actividad | MB por actividad | GB por recolector / periodo | Costo Hot por recolector / periodo | GB por 100 recolectores / periodo | Costo Hot por 100 recolectores / periodo |
|---|---|---|---|---|---|---|---|---|
| Conservador | 10 | 1 | 1 | 3 MB | 0.03 GB | USD 0.00 | 2.93 GB | USD 0.14 |
| Base operativa | 60 | 8 | 2 | 12 MB | 0.70 GB | USD 0.03 | 70.31 GB | USD 3.44 |
| Exigente | 200 | 20 | 5 | 30 MB | 5.86 GB | USD 0.29 | 585.94 GB | USD 28.65 |

> Lectura de negocio: el costo del **dato nuevo del mes** en Blob puede parecer bajo. El verdadero impacto economico aparece cuando esos GB se retienen por 5 o 7 anios, se replican o se mantienen en tier caliente sin lifecycle.

## Proyeccion de Blob Storage sobre la Curva de Recolectores

La siguiente tabla aplica la proyeccion real de recolectores del Excel a tres escenarios de multimedia. Esta lectura asume, de forma conservadora y explicita, que el rango de 10 a 200 actividades corresponde a un periodo mensual.

| Anio | Recolectores proyectados | Conservador GB / mes | Conservador USD / mes | Base GB / mes | Base USD / mes | Exigente GB / mes | Exigente USD / mes |
|---|---|---|---|---|---|---|---|
| 2026 | 7,800 | 228.52 | USD 11.17 | 5,484.38 | USD 268.19 | 45,703.12 | USD 2,234.88 |
| 2027 | 15,000 | 439.45 | USD 21.49 | 10,546.88 | USD 515.74 | 87,890.62 | USD 4,297.85 |
| 2028 | 24,600 | 720.70 | USD 35.24 | 17,296.88 | USD 845.82 | 144,140.62 | USD 7,048.48 |
| 2029 | 35,400 | 1,037.11 | USD 50.71 | 24,890.62 | USD 1,217.15 | 207,421.88 | USD 10,142.93 |
| 2030 | 46,800 | 1,371.09 | USD 67.05 | 32,906.25 | USD 1,609.12 | 274,218.75 | USD 13,409.30 |

Interpretacion financiera:

- en escenario base, solo el dato nuevo mensual de Blob Storage podria pasar de **USD 268/mes en 2026** a **USD 1,609/mes en 2030**;
- en escenario exigente, el almacenamiento nuevo mensual por si solo ya superaria el piso de infraestructura temprana;
- esta tabla no incluye replicas, operaciones, lifecycle, versionado, retencion acumulada ni egreso, por lo que debe leerse como piso del costo variable y no como techo.

## Tabla de Costo Estimado por Anio 2026-2030

Para transformar la proyeccion del Excel en una lectura economica anual util, se usa una regla simple y explicitamente conservadora:

```text
Costo_total_minimo_mensual = Piso_plataforma_actual_sin_blob + Blob_escenario
```

Donde:

- `Piso_plataforma_actual_sin_blob = USD 330.78/mes`;
- ese valor se obtiene del consolidado actual de `USD 334.94/mes`, reemplazando la linea historica de Blob usada en el estimado inicial (`USD 4.16/mes`) por la nueva proyeccion basada en el Excel.

Esta tabla representa un **costo total minimo proyectado**, porque aun no incrementa de forma explicita otras lineas que probablemente subiran con el tiempo, como compute, observabilidad, mensajeria, cache, backups o replicas.

| Anio | Piso plataforma mensual | Conservador mensual | Conservador anual | Base mensual | Base anual | Exigente mensual | Exigente anual |
|---|---|---|---|---|---|---|---|
| 2026 | USD 330.78 | USD 341.95 | USD 4,103.45 | USD 598.97 | USD 7,187.59 | USD 2,565.66 | USD 30,787.95 |
| 2027 | USD 330.78 | USD 352.27 | USD 4,227.23 | USD 846.52 | USD 10,158.27 | USD 4,628.63 | USD 55,543.58 |
| 2028 | USD 330.78 | USD 366.02 | USD 4,392.27 | USD 1,176.60 | USD 14,119.17 | USD 7,379.26 | USD 88,551.08 |
| 2029 | USD 330.78 | USD 381.49 | USD 4,577.94 | USD 1,547.93 | USD 18,575.18 | USD 10,473.71 | USD 125,684.52 |
| 2030 | USD 330.78 | USD 397.83 | USD 4,773.92 | USD 1,939.90 | USD 23,278.75 | USD 13,740.08 | USD 164,880.92 |

### Lectura por Cliente Proyectado

La siguiente tabla expresa el mismo costo minimo mensual, pero distribuido entre el numero de clientes proyectados por anio. Sirve para aproximar el umbral economico de una suscripcion promedio antes de incorporar margen, soporte, servicios profesionales o capas premium de resiliencia.

| Anio | Clientes proyectados | Conservador USD / cliente / mes | Base USD / cliente / mes | Exigente USD / cliente / mes |
|---|---|---|---|---|
| 2026 | 13 | USD 26.30 | USD 46.07 | USD 197.36 |
| 2027 | 23 | USD 15.32 | USD 36.81 | USD 201.24 |
| 2028 | 40 | USD 9.15 | USD 29.41 | USD 184.48 |
| 2029 | 61 | USD 6.25 | USD 25.38 | USD 171.70 |
| 2030 | 84 | USD 4.74 | USD 23.09 | USD 163.57 |

Interpretacion ejecutiva:

- en la medida que el numero de clientes crece, el piso de plataforma se diluye mejor y el costo medio minimo por cliente baja;
- en escenario base, el costo medio minimo por cliente podria moverse desde **USD 46.07/mes en 2026** hasta **USD 23.09/mes en 2030**, siempre que el crecimiento siga la curva del Excel;
- en escenario exigente, aun con dilucion por crecimiento, la multimedia podria empujar el costo medio minimo por cliente por encima de **USD 160/mes** hacia 2030;
- estas cifras no deben confundirse con precio final de venta: todavia faltan margen, operacion, soporte, contingencia, impuestos y posibles capas premium por retencion o SLA.

## Segunda Tabla: Costo Estimado con Escalamiento de Plataforma desde 2028

La tabla anterior es util como piso economico, pero mantiene congeladas varias lineas de infraestructura. Para una lectura mas realista, esta segunda tabla escala desde 2028 tres componentes que dificilmente permaneceran planos en una trayectoria de crecimiento como la del Excel:

- **Compute de aplicacion**: basado en el costo actual de Container Apps y Functions;
- **PostgreSQL**: basado en compute y almacenamiento base del consolidado actual;
- **Observabilidad**: incorporando una base mensual referencial de App Insights + Log Analytics.

Metodologia usada:

```text
Piso_fijo_no_escalado = USD 114.00/mes
Compute_base = USD 72.12/mes
PostgreSQL_base = USD 144.66/mes
Observabilidad_base = USD 8.00/mes
```

Reglas de escalamiento desde 2028:

```text
Compute_escalado = Compute_base x sqrt(Recolectores_anio / Recolectores_2026)
PostgreSQL_escalado = PostgreSQL_base x sqrt(Lotes_activos_anio / Lotes_activos_2026)
Observabilidad_escalada = Observabilidad_base x sqrt(Recolectores_anio / Recolectores_2026)
```

Entre 2026 y 2027 se conserva el baseline actual. Desde 2028 en adelante se aplica este crecimiento amortiguado para reflejar que la plataforma no escala de forma lineal pura, pero tampoco permanece fija.

### Componentes de Plataforma Escalados

| Anio | Compute mensual escalado | PostgreSQL mensual escalado | Observabilidad mensual escalada |
|---|---|---|---|
| 2026 | USD 72.12 | USD 144.66 | USD 8.00 |
| 2027 | USD 72.12 | USD 144.66 | USD 8.00 |
| 2028 | USD 128.08 | USD 300.06 | USD 14.21 |
| 2029 | USD 153.64 | USD 357.46 | USD 17.04 |
| 2030 | USD 176.66 | USD 407.68 | USD 19.60 |

### Costo Total Estimado con Plataforma Escalada

| Anio | Conservador mensual | Conservador anual | Base mensual | Base anual | Exigente mensual | Exigente anual |
|---|---|---|---|---|---|---|
| 2026 | USD 349.95 | USD 4,199.45 | USD 606.97 | USD 7,283.59 | USD 2,573.66 | USD 30,883.95 |
| 2027 | USD 360.27 | USD 4,323.23 | USD 854.52 | USD 10,254.27 | USD 4,636.63 | USD 55,639.58 |
| 2028 | USD 591.58 | USD 7,099.00 | USD 1,402.16 | USD 16,825.89 | USD 7,604.82 | USD 91,257.81 |
| 2029 | USD 692.86 | USD 8,314.33 | USD 1,859.30 | USD 22,311.57 | USD 10,785.08 | USD 129,420.91 |
| 2030 | USD 784.98 | USD 9,419.73 | USD 2,327.05 | USD 27,924.56 | USD 14,127.23 | USD 169,526.74 |

Interpretacion ejecutiva:

- esta segunda tabla deja de tratar la plataforma como un piso casi inmovil y, por tanto, se acerca mas a un escenario de operacion real;
- en escenario base, el costo mensual total podria pasar de **USD 606.97 en 2026** a **USD 2,327.05 en 2030** cuando ademas de Blob tambien crecen compute, PostgreSQL y observabilidad;
- el salto entre 2027 y 2028 es relevante porque coincide con el punto donde la curva del Excel ya justifica re-evaluar sizing y gobierno de plataforma;
- aun asi, la tabla sigue siendo prudente: no escala explicitamente Redis, Cosmos, Service Bus, API Management, backups avanzados, replicas geo ni componentes de Opcion C.

Como referencia adicional, en escenario base el costo medio mensual minimo por cliente con plataforma escalada podria pasar de **USD 46.69 en 2026** a **USD 27.70 en 2030**, asumiendo que la curva de clientes del Excel se cumple y que el crecimiento permite diluir mejor el piso compartido.

## Impacto de Retencion a 5 y 7 Anios

La siguiente tabla muestra el **volumen acumulado** y la **factura mensual de Hot Storage al final del periodo** si no existiera archivado ni limpieza, usando la misma unidad base y 100 recolectores como referencia.

| Escenario | GB nuevos por periodo | Volumen retenido al ano 1 | Factura mensual al ano 1 | Volumen retenido a 5 anios | Factura mensual a 5 anios | Volumen retenido a 7 anios | Factura mensual a 7 anios |
|---|---|---|---|---|---|---|---|
| Conservador | 2.93 GB | 35.16 GB | USD 1.72 | 175.78 GB | USD 8.60 | 246.09 GB | USD 12.03 |
| Base operativa | 70.31 GB | 843.75 GB | USD 41.26 | 4218.75 GB | USD 206.30 | 5906.25 GB | USD 288.82 |
| Exigente | 585.94 GB | 7031.25 GB | USD 343.83 | 35156.25 GB | USD 1719.14 | 49218.75 GB | USD 2406.79 |

### Interpretacion

- Si la retencion larga se mantiene en Hot Storage, el costo acumulado puede convertirse en una linea relevante del margen, incluso si el dato nuevo mensual parecia barato.
- Negocio debe tratar la retencion como una decision comercial y regulatoria, no como una consecuencia tecnica sin costo.
- La politica recomendada es mover evidencia historica a `Cool` o `Archive` segun acceso y valor probatorio.

## Costo Base de Plataforma

Aunque Blob Storage conecta bien con el negocio, la plataforma tiene un piso operativo que debe recuperarse con cargo base de suscripcion o con un numero minimo de clientes activos.

| Componente base | Referencia | Aproximacion mensual |
|---|---|---|
| PostgreSQL Flexible Server compute | `0.1532 USD/h` x `730 h` | USD 111.84 |
| Service Bus Standard base | `10 USD/mes` | USD 10.00 |
| Container Apps base referencial para 4 APIs con carga moderada | depende de segundos activos de vCPU y memoria | Variable, pero puede convertirse en el segundo piso operativo tras BD |
| Observabilidad, secretos y cache | validar en calculadora | Deben presupuestarse aparte para no subestimar el piso real |

## Como Debe Conectarse el Costo con Ingresos

La sugerencia para negocio es construir el pricing con dos capas:

1. **Cargo base por cliente**: cubre piso de plataforma, soporte, seguridad, monitoreo y parte del compute comun.
2. **Cargo variable o banda de consumo**: vinculado a recolectores activos, multimedia retenida, volumen de actividad o una combinacion de esos drivers.

### Mapeo sugerido ingreso-costo

| Driver comercial | Costo Azure que explica | Comentario |
|---|---|---|
| Cliente activo | parte del piso de PostgreSQL, mensajeria y soporte | ayuda a recuperar costo base del SaaS |
| Recolectores activos | compute de APIs, sincronizacion, logs | mejor proxy de uso operativo que solo contar clientes |
| Actividades registradas | crecimiento de BD y operaciones | explica intensidad transaccional |
| Imagenes y videos | Blob Storage, operaciones y retencion | driver mas claro para costo variable visible |
| Politica de retencion | storage historico, replicas y backup | debe tratarse como palanca comercial o contractual |
| SLA / resiliencia requerida | App Gateway, AKS, Service Bus Premium, HA | no todos los clientes deben financiar la misma resiliencia |

## Revision del Plan de Costos

El plan se afino respecto al brief base en estos puntos:

1. Se separo explicitamente el costo del dato nuevo del costo de retencion acumulada.
2. Se formalizo el uso de `Frecuencia` para evitar errores si el rango 10-200 no es mensual.
3. Se identifico que la arquitectura robusta no debe cargarse al cliente promedio si aun no existe necesidad contractual u operativa.
4. Se traslado el foco desde una cifra unica mensual a una lectura por drivers, que es mucho mas util para pricing SaaS.
5. Se incorporo la proyeccion comercial 2026-2030 para que el modelo ya no dependa solo de rangos abstractos, sino de una curva anual real de clientes, comunidades, recolectores y lotes activos.

## Recomendaciones Economicas

- Definir desde ahora una politica de lifecycle para Blob Storage y no esperar a que aparezca la primera sorpresa de costo.
- Medir separadamente `GB nuevos`, `GB retenidos`, `ingestion de logs` y `payloads de error` por tenant.
- Evitar trasladar a todos los clientes el costo de componentes enterprise si aun no generan ese nivel de riesgo o demanda.
- Revisar trimestralmente si el piso operativo por cliente mejora o empeora segun crece la base instalada.

## Referencias

- Arquitectura recomendada: [ARQ-PACHAMAMA-AZURE-ESCALAMIENTO-Y-PRICING-20260421.md](ARQ-PACHAMAMA-AZURE-ESCALAMIENTO-Y-PRICING-20260421.md)
- Brief base: [ARQ-PACHAMAMA-AZURE-PROYECCION-COSTOS-20260421.md](ARQ-PACHAMAMA-AZURE-PROYECCION-COSTOS-20260421.md)
- Azure Pricing Calculator: https://azure.microsoft.com/es-es/pricing/calculator/
- Azure Retail Prices API: https://prices.azure.com/api/retail/prices