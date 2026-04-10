---
name: azure-pricing
description: "Skill para calcular y estimar costos de recursos Azure. Usar cuando el usuario solicite: estimar costos de infraestructura Azure, calcular precio mensual o anual de recursos cloud, comparar tiers o SKUs de servicios Azure, generar informe de costos Azure, presupuestar una arquitectura cloud en Azure. Genera un archivo Markdown como entregable con el desglose de costos. Usa el MCP mcp-azure-pricing para consultar precios reales desde la Azure Retail Prices API."
---

# Azure Pricing — Estimacion de Costos

Genera estimaciones de costo de infraestructura Azure con desglose mensual y anual.
Usa la Azure Retail Prices API (datos reales) y entrega un informe Markdown estructurado.

## Referencia
- **API de precios**: https://prices.azure.com/api/retail/prices
- **Calculadora Azure**: https://azure.microsoft.com/es-es/pricing/calculator/

---

## Flujo de trabajo

### Paso 1 — Identificar el escenario

Recopilar del usuario:
1. **Nombre del escenario** (ej: "API REST produccion", "Plataforma de analisis de datos")
2. **Lista de recursos Azure** que necesita (VMs, bases de datos, almacenamiento, etc.)
3. **Region principal** (ej: East US, Brazil South, West Europe)
4. **Moneda** (default: USD)
5. **Patron de uso** por recurso (continuo 24/7 = 730 h/mes, horario laboral = ~176 h/mes, etc.)

Si el usuario no especifica alguno de estos datos, usa los defaults razonables e indicalos claramente en el informe.

Si el usuario pide recursos que no conoces en detalle, usa `listar_servicios_azure` para confirmar el nombre exacto.

---

### Paso 2 — Consultar precios reales

Para cada recurso del escenario:

1. Llama a `consultar_precios_azure` con el servicio, region y SKU/tier indicado.

```
consultar_precios_azure(
  servicio: "<nombre del servicio>",
  region: "<region>",
  filtro_sku: "<tier o tamaño>",   // opcional
  tipo: "Consumption",              // o "Reservation" si el usuario quiere precio reservado
  moneda: "USD",
  limite: 10
)
```

2. Del resultado, selecciona el SKU mas apropiado segun el requerimiento del usuario.
   - Prioriza `type: "Consumption"` para estimaciones por defecto
   - Si el usuario quiere reserva 1 o 3 años, usa `type: "Reservation"`
   - Para VMs: busca el SKU que coincida con vCPU/RAM solicitados (ej: "D2 v3" = 2 vCPU, 8 GB RAM)

3. Anota:
   - `retailPrice` = precio por unidad
   - `unitOfMeasure` = unidad (puede ser "1 Hour", "1 GB", "1/Month", "10K", etc.)

---

### Paso 3 — Calcular la estimacion

Con todos los precios obtenidos, llama a `calcular_estimacion_costo`:

```
calcular_estimacion_costo(
  nombre_estimacion: "<nombre del escenario>",
  moneda: "USD",
  items: [
    {
      nombre: "<descripcion del recurso>",
      servicio: "<nombre servicio Azure>",
      sku: "<SKU seleccionado>",
      region: "<region>",
      precio_unitario: <retailPrice de la API>,
      unidad: "<unitOfMeasure>",
      cantidad: <unidades por mes>,          // ej: 730 para 1 hora * 730 h/mes
      cantidad_instancias: <numero>,          // replicas o instancias
      notas: "<notas opcionales>"
    },
    ...
  ]
)
```

#### Guia de conversion de unidades a cantidad mensual

| unitOfMeasure | Descripcion | cantidad tipica |
|---|---|---|
| `1 Hour` | Precio por hora | 730 (24/7) \| 176 (horario laboral) |
| `1/Month` | Precio fijo mensual | 1 |
| `1 GB` | Precio por GB almacenado | GB que usara el recurso |
| `10 GB` | Precio por cada 10 GB | GB_totales / 10 |
| `100 GB` | Precio por cada 100 GB | GB_totales / 100 |
| `1 GB/Month` | Precio por GB/mes | GB mensuales |
| `1 vCore/Month` | Precio por vCore mensual | numero de vCores |
| `10K` | Precio por cada 10K transacciones | transacciones_totales / 10000 |
| `1M` | Precio por millon | total / 1000000 |

---

### Paso 4 — Generar el informe Markdown

Crea el archivo usando `create_file` con la siguiente plantilla:

**Ruta del archivo**: `azure-costos/AZURE-COSTOS-<ESCENARIO-SLUG>_<YYYYMMDD>.md`

Donde `<ESCENARIO-SLUG>` es el nombre del escenario en mayusculas con guiones (ej: `API-REST-PRODUCCION`).

---

## Plantilla del informe

```markdown
# Estimacion de Costos Azure
## <nombre_estimacion>

**Fecha:** <fecha actual DD de mes de YYYY>
**Region principal:** <region>
**Moneda:** <moneda>
**Tipo de precio:** Consumo bajo demanda (Pay-as-you-go) | Reserva 1 año | Reserva 3 años
**Referencia:** [Azure Pricing Calculator](https://azure.microsoft.com/es-es/pricing/calculator/)

---

## Resumen Ejecutivo

| Concepto | Valor |
|---|---|
| **Costo Mensual Estimado** | <moneda> <total_mensual> |
| **Costo Anual Estimado** | <moneda> <total_anual> |
| **Numero de recursos** | <cantidad de items> |

---

## Desglose de Recursos

| # | Recurso | Servicio Azure | SKU / Tier | Region | Precio Unit. | Unidad | Cant./Mes | Instancias | Costo Mensual | Costo Anual |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | <nombre> | <servicio> | <sku> | <region> | <moneda> <precio_unitario> | <unidad> | <cantidad> | <instancias> | <moneda> <costo_mensual> | <moneda> <costo_anual> |
| ... | | | | | | | | | | |
| | | | | | | | **TOTAL** | | **<moneda> <total_mensual>** | **<moneda> <total_anual>** |

---

## Notas y Supuestos

- Los precios se obtienen de la [Azure Retail Prices API](https://prices.azure.com/api/retail/prices) y pueden variar.
- Se asumen **730 horas/mes** para recursos que corren 24/7.
- Los precios NO incluyen impuestos locales ni descuentos de EA/MCA.
- Tipo de precio utilizado: **Consumption** (pago por uso) salvo indicacion contraria.
- Para obtener precios exactos, usar la [calculadora oficial de Azure](https://azure.microsoft.com/es-es/pricing/calculator/).

### Supuestos por recurso
<lista de supuestos especificos como uso de horas, GB de storage, transacciones esperadas, etc.>

---

## Recomendaciones de Optimizacion

<Si aplica, incluir recomendaciones como:>
- Usar Reserved Instances para recursos de uso 24/7 (ahorro ~30-50%)
- Tiers mas economicos disponibles
- Alternativas serverless si el uso es intermitente

---

*Informe generado automaticamente con datos de la Azure Retail Prices API.*
*Fecha de generacion: <fecha y hora>*
```

---

## Reglas importantes

1. **Nunca inventes precios**: usa SIEMPRE los valores de `retailPrice` que retorna `consultar_precios_azure`.
2. Si la API no retorna resultados para un recurso, indicalo en el informe con "Precio no disponible via API — consultar manualmente en https://azure.microsoft.com/es-es/pricing/calculator/".
3. **730 horas/mes** es el estandar para VMs y recursos por hora corriendo 24/7.
4. Para recursos con precio `1/Month`, la `cantidad` es siempre `1`.
5. Siempre incluir el enlace a la calculadora oficial como referencia.
6. El archivo debe guardarse en la carpeta `azure-costos/` del workspace.
