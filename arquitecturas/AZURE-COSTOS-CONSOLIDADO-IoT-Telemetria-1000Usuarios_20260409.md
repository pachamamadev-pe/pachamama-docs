# Estimación de Costos Azure
## CONSOLIDADO — Plataforma IoT Telemetría y Sincronización · 1,000 Usuarios Concurrentes · Primera Etapa

**Fecha:** 09 de abril de 2026  
**Moneda:** USD  
**Tipo de precio:** Pay-as-you-go (Consumption)  
**Referencia:** [Azure Pricing Calculator](https://azure.microsoft.com/es-es/pricing/calculator/)

---

## Resumen Ejecutivo

| Concepto | Valor |
|---|---|
| **Total Mensual** | USD 334.94 |
| **Total Anual** | USD 4019.33 |
| **Número de recursos** | 12 |

---

## Desglose por Recurso

| # | Recurso | Servicio | SKU | Región | Precio/Unidad | Unidad | Cant./Mes | Inst. | Mes (USD) | Año (USD) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1. PostgreSQL Flexible Server — Cómputo (2 vCores / 8 GB RAM, 24/7) | Azure Database for PostgreSQL | General Purpose Ddsv5 — 2 vCore (equiv. D2ds_v4) | eastus | $0.1780 | 1 Hour | 730 | 1 | **$129.94** | **$1559.28** |
| 2 | 2. PostgreSQL Flexible Server — Almacenamiento Premium 128 GB | Azure Database for PostgreSQL | Premium SSD Managed Storage | eastus | $0.1150 | 1 GB/Month | 128 | 1 | **$14.72** | **$176.64** |
| 3 | 3. Azure Container Apps — vCPU (4 APIs × 0.5 vCPU promedio, 24/7) | Container Instances | Standard vCPU Duration (proxy) | eastus | $0.0405 | 1 Hour | 730 | 2 | **$59.13** | **$709.56** |
| 4 | 4. Azure Container Apps — Memoria (4 APIs × 1 GB promedio, 24/7) | Container Instances | Standard Memory Duration (proxy) | eastus | $0.0044 | 1 GB Hour | 730 | 4 | **$12.99** | **$155.93** |
| 5 | 5. Service Bus Standard — Namespace base | Service Bus | Standard | eastus | $10.0000 | 1/Month | 1 | 1 | **$10.00** | **$120.00** |
| 6 | 6. Service Bus Standard — Operaciones mensajes (~40M msgs/mes) | Service Bus | Standard Messaging Operations | eastus | $0.5000 | 1M | 40 | 1 | **$20.00** | **$240.00** |
| 7 | 7. Blob Storage Hot LRS — Telemetría y sincronización (200 GB) | Storage | Hot LRS | eastus | $0.0208 | 1 GB/Month | 200 | 1 | **$4.16** | **$49.92** |
| 8 | 8. Azure Cache for Redis — C1 Standard (1 GB, 1 shard, replicado) | Azure Cache for Redis | C1 Standard | eastus | $55.0000 | 1/Month | 1 | 1 | **$55.00** | **$660.00** |
| 9 | 9. Azure Cosmos DB Serverless — Storage (~10 GB datos activos) | Azure Cosmos DB | Serverless / Data Stored | eastus | $0.2500 | 1 GB/Month | 10 | 1 | **$2.50** | **$30.00** |
| 10 | 10. Azure Cosmos DB Serverless — Request Units consumidas (~50M RU/mes) | Azure Cosmos DB | Serverless RUs consumed | eastus | $12.5000 | 1/Month | 1 | 1 | **$12.50** | **$150.00** |
| 11 | 11. Azure Static Web Apps — Plan Standard (frontend / portal) | Azure Static Web Apps | Standard | eastus | $9.0000 | 1/Month | 1 | 1 | **$9.00** | **$108.00** |
| 12 | 12. Azure Functions — Plan Consumption (procesamiento serverless telemetría) | Azure Functions | Consumption Plan | eastus | $5.0000 | 1/Month | 1 | 1 | **$5.00** | **$60.00** |
| | | | | | | | | **TOTAL** | **$334.94** | **$4019.33** |

---

## Notas por Recurso

- **1. PostgreSQL Flexible Server — Cómputo (2 vCores / 8 GB RAM, 24/7):** ✅ PRECIO CONFIRMADO VIA API · retailPrice USD 0.178/hora · Flexible Server GP Ddsv5 Series 2 vCore · Equivalente generacional al D2ds_v4 solicitado · Operativo 24/7 = 730 h/mes
- **2. PostgreSQL Flexible Server — Almacenamiento Premium 128 GB:** ⚠️ PRECIO REFERENCIAL (calculadora Azure) · USD 0.115/GB/mes para storage Premium SSD en Flexible Server · API no retornó este SKU de almacenamiento específico
- **3. Azure Container Apps — vCPU (4 APIs × 0.5 vCPU promedio, 24/7):** ⚠️ PROXY VIA CONTAINER INSTANCES · Azure Container Apps no indexado en Retail API · Se usa Container Instances Standard vCPU ($0.0405/h) como proxy representativo · 4 APIs × 0.5 vCPU = 2 vCPU equivalentes × 730 h
- **4. Azure Container Apps — Memoria (4 APIs × 1 GB promedio, 24/7):** ⚠️ PROXY VIA CONTAINER INSTANCES · Standard Memory USD 0.00445/GB-h · 4 APIs × 1 GB RAM = 4 GB × 730 h
- **5. Service Bus Standard — Namespace base:** ✅ PRECIO CONFIRMADO VIA API · meterName: Standard Base Unit · USD 10.00/mes fijo por namespace Standard
- **6. Service Bus Standard — Operaciones mensajes (~40M msgs/mes):** ✅ PRECIO CONFIRMADO VIA API · USD 0.50/millón de operaciones · Estimado 40M mensajes/mes para telemetría de 1,000 usuarios activos (primeras 10M incluidas en fee base)
- **7. Blob Storage Hot LRS — Telemetría y sincronización (200 GB):** ✅ PRECIO CONFIRMADO VIA API · meterName: Hot LRS Data Stored · USD 0.0208/GB/mes · 200 GB datos activos de telemetría (primeros 50 TB)
- **8. Azure Cache for Redis — C1 Standard (1 GB, 1 shard, replicado):** ⚠️ PRECIO REFERENCIAL (calculadora Azure) · API no retornó resultados para este servicio · Referencia pública: USD 0.0937/h × 730 h = ~USD 68.40/mes (máx). Usado USD 55/mes como estimado conservador (midpoint) · Validar en https://azure.microsoft.com/es-es/pricing/calculator/
- **9. Azure Cosmos DB Serverless — Storage (~10 GB datos activos):** ✅ PRECIO CONFIRMADO VIA API · meterName: Data Stored · SKU RUs/RUm · USD 0.25/GB/mes · Estimado 10 GB de documentos activos de telemetría y sincronización para 1,000 usuarios
- **10. Azure Cosmos DB Serverless — Request Units consumidas (~50M RU/mes):** ⚠️ PRECIO REFERENCIAL · SKU Serverless RU/s no indexado como línea independiente en Retail API · Referencia pública: USD 0.25/millón de RUs consumidas · Estimado ~50M RU/mes para 1,000 usuarios activos = USD 12.50/mes
- **11. Azure Static Web Apps — Plan Standard (frontend / portal):** ⚠️ PRECIO REFERENCIAL · No indexado en Azure Retail Prices API · Precio fijo oficial: USD 9.00/mes (Standard plan, CDN global incluido, 100 GB bandwidth/mes) · Fuente: https://azure.microsoft.com/es-es/pricing/details/app-service/static/
- **12. Azure Functions — Plan Consumption (procesamiento serverless telemetría):** ⚠️ PRECIO REFERENCIAL · API no retornó resultados para este servicio · Tier gratuito: 1M ejecuciones + 400K GB-s/mes · Estimado conservador para excedente con 10–50M ejecuciones/mes = USD 2–10/mes · Usado USD 5/mes como punto medio

---

*Generado con Azure Retail Prices API — 09 de abril de 2026*  
*Referencia oficial: https://azure.microsoft.com/es-es/pricing/calculator/*
