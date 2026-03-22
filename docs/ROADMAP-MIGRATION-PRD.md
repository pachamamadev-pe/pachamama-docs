# Roadmap: Pase a Producción y Migración a Azure

Este documento describe las fases estratégicas para evolucionar la arquitectura MVP construida hacia un entorno de producción formal y unificado dentro un esquema corporativo (SaaS) utilizando Microsoft Azure como proveedor central.

---

## Fase 1: Migración de Recursos Azure Nativos a la Cuenta Corporativa

Actualmente existen recursos y lógicas Serverless que fueron abastecidas desde la cuenta personal (jecridosantos@outlook.com). Esta primera fase implica un "Lift & Shift" de configuraciones hacia el nuevo Tenant Microsoft garantizando orden a nivel de naming conventions.

- **Cuenta Destino (Tenant Corporativo):** pachamamadev@pachamaxter.onmicrosoft.com

### Propuesta de Nomenclatura (Naming Conventions)
Adaptado de [Azure Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming):

- **Grupos de Recursos (Resource Group):** g-<proyecto>-<entorno>-<region> (Ej. g-pachamama-prd-eastus)
- **Cuentas de Almacenamiento (Storage Account):** st<proyecto><entorno><region><correlativo> *Solo minúsculas, max 24 char.* (Ej. stpmamaprdeastus001)
- **Service Bus Namespace:** sb-<proyecto>-<entorno>-<region> (Ej. sb-pachamama-prd-eastus)
- **Azure Functions:** unc-<proyecto>-<módulo>-<entorno> (Ej. unc-pachamama-sas-prd)
- **App Service Plan (Para Serverless/Web):** plan-<proyecto>-<entorno>-<region>

### Mapa de Transferencia (Inventario a Migrar)

| Componente | Instancia Actual (Personal) | Propuesta Nuevo Nombre (Corporativo Prd) |
|---|---|---|
| **Resource Group** | n/a | g-pachamama-prd-eastus |
| **Blob Storage** | sapachamama001 | stpmamaprdeastus001 |
| **Service Bus** | pachamama-sync-batch | sb-pachamama-prd-eastus |
| **Funciones SAS** | pachamama-func-sas-node | unc-pachamama-sas-prd |
| **Funciones Sync** | pachamama-func-trace-sync | unc-pachamama-tracesync-prd |

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

La arquitectura MVP actual se distingue por ser **Híbrida Multicloud** (Heroku + Vercel + Railway + Azure + MongoDB).
El paso evolutivo del producto corresponde a consolidar todas las cargas y servicios computacionales en Azure, desplegando una **Arquitectura Mínima Viable** capaz de proveer un entorno de producción (Prd) estandarizado y resiliente.

> **Estado: [Por Definir - TBD]**

### Alcances Previstos para la Fase 3:
* **Contenedores de Backend (Java APIs):** Migración dinámica (Azure Container Apps o Azure App Service for Containers) en reemplazo de Heroku Dynos.
* **Frontend Apps (React/Vite):** Utilización de Azure Static Web Apps en reemplazo de Vercel.
* **Bases de Datos & Caché:** Posible adopción nativa (Redis Enterprise, Azure Database for PostgreSQL flexible) dependiendo del presupuesto inicial.
* Este análisis detallado se trazará como una fase propia en la siguiente evolución arquitectónica documentada.
