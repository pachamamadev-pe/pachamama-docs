# Roadmap: Pase a Producción y Migración a Azure

Este documento describe las fases estratégicas para evolucionar la arquitectura MVP construida hacia un entorno de producción formal y unificado dentro un esquema corporativo (SaaS) utilizando Microsoft Azure como proveedor central.

---

## Fase 1: Migración de Recursos Azure Nativos a la Cuenta Corporativa

Actualmente existen recursos y lógicas Serverless que fueron abastecidas desde la cuenta personal (jecridosantos@outlook.com). Esta primera fase implica un "Lift & Shift" de configuraciones hacia el nuevo Tenant Microsoft garantizando orden a nivel de naming conventions.

- **Cuenta Destino (Tenant Corporativo):** pachamamadev@pachamaxter.onmicrosoft.com

### Propuesta de Nomenclatura (Naming Conventions)
Adaptado de [Azure Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming):

- **Grupos de Recursos (Resource Group):** 
g-<proyecto>-<entorno>-<region> (Ej. 
g-pachamama-prd-eastus)
- **Cuentas de Almacenamiento (Storage Account):** st<proyecto><entorno><region><correlativo> *Solo minúsculas, max 24 char.* (Ej. stpmamaprdeastus001)
- **Service Bus Namespace:** sb-<proyecto>-<entorno>-<region> (Ej. sb-pachamama-prd-eastus)
- **Azure Functions:** func-<proyecto>-<módulo>-<entorno> (Ej. func-pachamama-sas-prd)
- **App Service Plan (Para Serverless/Web):** plan-<proyecto>-<entorno>-<region>

### Mapa de Transferencia (Inventario a Migrar)

| Componente | Instancia Actual (Personal) | Propuesta Nuevo Nombre (Corporativo Prd) |
|---|---|---|
| **Resource Group** | n/a | 
g-pachamama-prd-eastus |
| **Blob Storage** | sapachamama001 | stpmamaprdeastus001 |
| **Service Bus** | pachamama-sync-batch | sb-pachamama-prd-eastus |
| **Funciones SAS** | pachamama-func-sas-node | func-pachamama-sas-prd |
| **Funciones Sync** | pachamama-func-trace-sync | func-pachamama-tracesync-prd |

*Acción Requerida:* Desplegar la infraestructura usando la nueva cuenta, validar conectividad de las colas e insertar las nuevas AZURE_STORAGE_ACCOUNT... y AZURE_SERVICEBUS_CONNECTION_STRING dentro del backend Java.

---

## Fase 2: Segregación Operativa de Bases de Datos (Railway)

Previo al pase final, la actual capa de datos operacional PostgreSQL (con PostGIS) no debe mezclar información de pruebas y del release.

Se mantendrá el alojamiento en la actual cuenta centralizada en **Railway** (pachamamadev@gmail.com), pero se instanciará una base de separación en el mismo cluster.

### Distribución de Entornos
1. **Entornos Previos (Local / Dev / Staging):**
   * Base de Datos Actual: pachamama_db
   * Redirección a: pachamama_db_dev
2. **Entorno de Producción (PRD):**
   * Base de Datos Nueva: pachamama_db_prd
   * Objetivo: Proveer la conexión de backend final desde la URL jdbc:postgresql://<railway-host>:<port>/pachamama_db_prd bajo un secreto aislado y credenciales independientes.

---

## Fase 3: Migración Integral de Servicios Cloud Hacia Azure SaaS

La arquitectura MVP actual se distingue por ser **Híbrida Multicloud** (Heroku + Vercel + Railway + MongoDB).
El paso evolutivo consiste en consolidar la infraestructura base dentro de Azure, logrando gobernanza centralizada, seguridad perimetral y soporte para alta concurrencia (Estimación inicial: 10 clientes x 100 usuarios activos = **~1000 usuarios concurrentes** promedio).

### Arquitectura Propuesta (Azure Nativo)

Esta primera versión "SaaS" se alinea a los servicios administrados de Azure (PaaS/Serverless) para maximizar la auto-escalabilidad sin incurrir en mantenimiento profundo de servidores (IaaS).

`mermaid
architecture-beta
    group api(cloud)[Azure Nube Corporativa PRD]

    service webadmin(internet)[Azure Static Web Apps] in api
    service mobil(mobile)[Mobile App Android]
    
    service aca(server)[Azure Container Apps\n(Microservicios Java)] in api
    service func(server)[Azure Functions\n(NodeJS / Serverless)] in api
    
    service pgsql(database)[Azure DB PostgreSQL\nFlexible Server] in api
    service cosmos(database)[Azure Cosmos DB\nfor MongoDB] in api
    service redis(database)[Azure Cache\nfor Redis] in api
    
    service bus(database)[Azure Service Bus] in api
    service blob(disk)[Azure Blob Storage] in api
    
    webadmin --> aca
    mobil --> func
    mobil --> aca
    
    aca --> pgsql
    aca --> cosmos
    aca --> redis
    aca --> bus
    func --> blob
    func --> bus
    
    bus --> aca
`

*(Diagrama Lógico de Interacciones Core centralizado en Azure)*

### Inventario de Recursos a Provisionar (Alta Concurrencia MVP+)

Bajo la nomenclatura propuesta, la infraestructura soportará picos aislados de la fuerza de recolección y sincronización masiva valiéndose de Azure Container Apps (KEDA).

| Capa | Recurso Azure | Nomenclatura (Ej. East US) | Tamaño / SKU Recomendado (Para 1000 usuarios) |
|---|---|---|---|
| **Frontend Web** | Azure Static Web Apps | swa-web-admin-prd <br> swa-web-landing-prd | Standard Plan (S1) - Custom domains y ancho de banda. |
| **Orquestador** | Azure Container Apps Env | cae-pachamama-prd-eastus | Consumption (Serverless) - Facturación por invocación y CPU reservado. |
| **Api Admin** | Azure Container App | ca-api-admin-prd | 0.5 vCPU / 1GB RAM (Escala Mínima 1, Máx 5) |
| **Api Sync** | Azure Container App | ca-api-sync-prd | 0.5 vCPU / 1GB RAM (Escala por eventos del bus) |
| **Api Notify** | Azure Container App | ca-api-notif-prd | 0.25 vCPU / 0.5GB RAM |
| **Api Trace** | Azure Container App | ca-api-trace-prd | 0.5 vCPU / 1GB RAM |
| **DB Relacional** | Azure PostgreSQL | psql-pachamama-prd-eastus | Flexible Server - **General Purpose D2ds_v4** (2 vCores, 8GB RAM). |
| **DB NoSQL** | Azure Cosmos DB (Mongo) | cosmos-pachamama-prd-eastus | Capacity Mode: **Serverless** (Pago estricto por RU/s consumido). |
| **Caché** | Azure Cache for Redis | edis-pachamama-prd-eastus | Standard **C1** (1 GB) - Alta disponibilidad de nodos. |
| **Mensajería** | Azure Service Bus | sb-pachamama-prd-eastus | **Standard Tier** - Soporte de Colas y Tópicos. |
| **Archivos** | Azure Blob Storage | stpmamaprdeastus001 | **Standard General Purpose V2** (LRS). |
| **Serverless Ops**| Azure Functions | unc-sas-prd <br> unc-tracesync-prd | Consumption Plan (Y1). |

*(Nota: Los servicios de proveedores terceros orientados a dominio como Twilio y Firebase persistirán agnósticos a la nube).*

### Estimación Financiera y Tiempos de Implementación

**1. Tiempos de Implementación Estimados (Time-to-Market)**

*   **Infraestructura como Código (Bicep/Terraform):** 1.5 a 2 semanas.
*   **Refactorización de Redes Privadas y Seguridad:** 1 semana.
*   **Migración de Datos (Railway -> Postgres, Atlas -> Cosmos):** 1 a 1.5 semanas. (Extracción y compatibilidad de PostGIS).
*   **Migración de Pipelines CI/CD (GitHub Actions -> ACA/SWA):** 1 semana.
*   **Pruebas de Carga (Stress Testing - 1000 users) y QA:** 1 semana.
*   **Total de Ejecución:** **~5 a 6 Semanas** (1.5 Meses con equipo de Cloud/DevOps dedicado).

**2. Costo Promedio Referencial (Azure Monthly Estimate)**

Basado en la operatividad concurrente de aproximada 1000 usuarios activos enviando datos de telemetría y sincronización:

*   **Azure DB PostgreSQL (D2ds_v4):** ~.00 / mes (Backbone relacional principal).
*   **Azure Container Apps (Consumo Promedio ~4 APIs):** ~.00 - .00 / mes.
*   **Azure Cache for Redis (C1 Standard):** ~.00 / mes.
*   **Azure Cosmos DB (Serverless):** ~.00 a .00 / mes.
*   **Azure Static Web Apps (Standard):** ~.00 / mes.
*   **Service Bus, Blob Storage, Functions (Serverless):** ~.00 - .00 / mes.
*   **Total Referencial Mensual:** **~.00 - .00 USD / mes** 

*(Nota: Posterior a la maduración, se puede optar por "Reserved Instances" de 1 a 3 años para la Base de Datos PostgreSQL y Redis bajando un ~30-40% el costo recurrente).*
