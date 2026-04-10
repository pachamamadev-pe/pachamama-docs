# Arquitectura Cloud — Pachamama: Migración Completa a Azure (SaaS)

**Empresa / Cliente**: Pachamama (REORI CORP S.A.C.)  
**Versión**: 2.0  
**Fecha**: 10 de Abril de 2026  
**Revisión**: Inicio de migración ajustado a Junio 2026; costos actuales corregidos (Heroku $80, Vercel $0, Railway $5, Azure Personal $2)  
**Proveedor Principal**: Microsoft Azure  
**Preparado por**: Arquitecto Cloud Expert (GitHub Copilot)  
**Alcance**: Migración total — Heroku + Vercel + Railway + MongoDB Atlas → Azure Nativo  
**Costo Mensual Objetivo**: ~USD 334.94 (consolidado verificado con Azure Retail Prices API)  
**Documento previo**: [ARQ-PACHAMAMA-AZURE-20260410.md](./ARQ-PACHAMAMA-AZURE-20260410.md) *(Fase 1 — recursos serverless)*  
**Versión anterior**: [ARQ-PACHAMAMA-AZURE-FULL-20260410.md](./ARQ-PACHAMAMA-AZURE-FULL-20260410.md)

---

## Resumen Ejecutivo

Pachamama opera su MVP con una arquitectura híbrida distribuida en cuatro proveedores distintos: **Heroku** (backends Java), **Vercel** (frontend web), **Railway** (PostgreSQL), **MongoDB Atlas** (NoSQL), más los recursos Azure ya existentes. Esta dispersión genera latencia entre servicios, eleva el riesgo operativo de seguridad por la gestión de credenciales en proveedores separados, y dificulta la gobernanza centralizada necesaria para escalar a un modelo SaaS con múltiples clientes.

El objetivo de esta migración es **consolidar toda la infraestructura en Microsoft Azure**, eliminando las dependencias externas de cómputo y datos. La decisión se sustenta en: (1) reducción de latencia interna al tener todos los servicios en la misma red, (2) gobernanza unificada de identidad y secretos vía Azure Entra ID y Key Vault, (3) escalabilidad nativa para los ~1,000 usuarios concurrentes proyectados, y (4) preparación de la plataforma para modelo SaaS multi-tenant (10 clientes × 100 usuarios).

El consolidado de costos verificado con la Azure Retail Prices API establece un costo mensual objetivo de **USD 334.94/mes** (~USD 4,019/año) con arquitectura Pay-as-you-go, con potencial de reducción del 30–40% al activar Reserved Instances en el año 2.

Este documento presenta **tres estrategias de migración** hacia la misma arquitectura objetivo Azure. Se diferencian en la velocidad de transición, el tiempo de costos dobles y el nivel de riesgo de impacto al servicio activo. La **Opción A — Migración por Olas** es la recomendada para minimizar el impacto operativo, con inicio planificado para **Junio 2026**.

Los servicios de identidad (Firebase Auth, FCM) y comunicaciones externas (Twilio) **no son migrados** ya que son agnósticos al proveedor cloud y no hay equivalente Azure con igual madurez para estas funciones específicas.

---

## Supuestos

| # | Supuesto | Impacto si es Incorrecto |
|---|----------|--------------------------|
| 1 | Las APIs Java en Heroku se pueden containerizar sin cambios de código (solo variables de entorno) | Si hay dependencias del dyno Heroku, requerirá refactorización previa |
| 2 | La base de datos Railway PostgreSQL + PostGIS migra a Azure PostgreSQL Flexible Server con `pg_dump` + `pg_restore` sin pérdida de datos | Si hay extensiones no soportadas, requiere validación de compatibilidad |
| 3 | MongoDB Atlas (colecciones `pachamama_notifications`, `pachamama_traceability_readmodel_dev`) migra a Cosmos DB API MongoDB sin cambios en el código de los backends | Las operaciones avanzadas de MongoDB (aggregation pipelines) deben validarse en Cosmos DB |
| 4 | Redis Labs (Azure East US) migra a Azure Cache for Redis C1 Standard con export/import de snapshot | Los TTLs y estructuras de datos simples son totalmente compatibles |
| 5 | Firebase Auth y FCM se mantienen como proveedores externos; los backends validan JWT de Firebase contra Azure API Management | Ninguno — Firebase permanece fuera del scope de migración |
| 6 | Twilio (OTP por WhatsApp) se mantiene como proveedor externo | Ninguno — Twilio permanece fuera del scope |
| 7 | El equipo puede mantener costos dobles (Azure + proveedores actuales) durante el período de transición (~4–8 semanas según opción) | Si el presupuesto no lo permite, se debe acelerar el cutover |
| 8 | La suscripción corporativa Azure tiene cuota suficiente para todos los SKUs requeridos en la región elegida (inicialmente brazilsouth) | Solicitar aumentos de cuota con 1 semana de anticipación a cada wave |
| 9 | ~1,000 usuarios concurrentes como pico de carga; la estimación de costos se basa en este valor | Si la carga real supera este pico, los costos de Container Apps y Service Bus suben proporcionalmente |
| 10 | El equipo tiene acceso a los repositorios GitHub de todos los servicios para crear Dockerfiles y pipelines CI/CD | Si algún repositorio está inaccesible, la containerización se bloquea |

---

## Contexto del Sistema

### Estado Actual (Antes de la Migración)

```
┌──────────────────────────────────────────────────────────────────────┐
│                     ARQUITECTURA ACTUAL (MVP)                        │
├─────────────────┬──────────────────────────────────────────────────  │
│  PROVEEDOR      │  SERVICIO                                          │
├─────────────────┼────────────────────────────────────────────────────│
│  Azure Personal │  Functions SAS + Trace, Blob Storage, Service Bus  │
│  Heroku         │  4 APIs Java (admin, sync, notifications, trace)    │
│  Vercel         │  Web Admin (React) + Web Landing                   │
│  Railway        │  PostgreSQL 16 + PostGIS                           │
│  MongoDB Atlas  │  pachamama_notifications + traceability_readmodel  │
│  Redis Labs     │  Redis v8.2 (caché geoespacial y OTP)              │
│  Firebase       │  Auth + FCM (se mantiene)                          │
│  Twilio         │  OTP WhatsApp (se mantiene)                        │
└─────────────────┴────────────────────────────────────────────────────┘
```

### Estado Objetivo (Post-Migración Azure)

```
┌──────────────────────────────────────────────────────────────────────┐
│                   ARQUITECTURA OBJETIVO (Azure SaaS)                 │
├─────────────────┬──────────────────────────────────────────────────  │
│  PROVEEDOR      │  SERVICIO                                          │
├─────────────────┼────────────────────────────────────────────────────│
│  Azure Corp     │  Container Apps (4 APIs Java) — reemplaza Heroku   │
│  Azure Corp     │  Static Web Apps (Admin + Landing) — reemplaza Vercel│
│  Azure Corp     │  PostgreSQL Flexible Server — reemplaza Railway    │
│  Azure Corp     │  Cosmos DB (MongoDB API) — reemplaza Atlas         │
│  Azure Corp     │  Azure Cache for Redis — reemplaza Redis Labs      │
│  Azure Corp     │  Functions SAS + Trace, Blob Storage, Service Bus  │
│  Azure Corp     │  Key Vault, App Insights, Log Analytics            │
│  Firebase       │  Auth + FCM (se mantiene — sin cambios)            │
│  Twilio         │  OTP WhatsApp (se mantiene — sin cambios)          │
└─────────────────┴────────────────────────────────────────────────────┘
```

### Mapa de Equivalencias de Migración

| Servicio Origen | Proveedor Origen | Servicio Azure Destino | Estrategia |
|----------------|-----------------|----------------------|------------|
| 4 Dynos Java (eco/basic) | Heroku | Azure Container Apps (Consumption) | Containerizar → CI/CD → Traffic shift |
| Web Admin (React) | Vercel | Azure Static Web Apps Standard | Re-deploy directo, misma build |
| Web Landing (Next.js/static) | Vercel | Azure Static Web Apps Standard | Re-deploy directo |
| PostgreSQL 16 + PostGIS | Railway | Azure DB PostgreSQL Flexible GP D2ds_v4 | pg_dump → pg_restore → dual-read |
| MongoDB (notifications) | MongoDB Atlas | Azure Cosmos DB (MongoDB API) Serverless | mongodump → mongorestore |
| MongoDB (traceability RM) | MongoDB Atlas | Azure Cosmos DB (MongoDB API) Serverless | mongodump → mongorestore |
| Redis v8.2 | Redis Labs | Azure Cache for Redis C1 Standard | export RDB → import |
| Functions + Storage + Service Bus | Azure Personal | Azure Corporativo (Fase 1 — ya planificada) | Lift & Shift |

### Requisitos No Funcionales (Post-Migración)

| Requisito | Valor Objetivo |
|-----------|---------------|
| Usuarios Concurrentes | ~1,000 (10 clientes × 100 activos) |
| Disponibilidad SLA | ≥ 99.5% (Container Apps Consumption) |
| Latencia Inter-Servicio (P95) | < 10 ms (misma VNet/región) vs ~50–200 ms actual entre proveedores |
| Latencia API desde LATAM (P95) | < 80 ms (brazilsouth) |
| RPO (Recovery Point Objective) | ≤ 1 hora (PostgreSQL con backups automáticos) |
| RTO (Recovery Time Objective) | ≤ 4 horas |
| Secrets en código fuente | 0 — Key Vault centralizado |
| Costo Mensual Objetivo | ~USD 334.94/mes (verificado con Retail API) |

---

## Arquitectura Objetivo — Azure Nativo

### Diagrama de Arquitectura Completa

```mermaid
flowchart LR
    subgraph Clientes
        APP[📱 Mobile Android\nPerú/LATAM]
        WEB[🖥️ Navegador\nAdmin/Landing]
    end

    subgraph External["🔗 Servicios Externos (se mantienen)"]
        FIREBASE[Firebase Auth\n+ FCM]
        TWILIO[Twilio\nOTP WhatsApp]
        PERUDEV[api.perudevs.com\nDNI/RUC]
    end

    subgraph AzureCorp["☁️ Azure Corporativo — Tenant REORI CORP S.A.C."]
        direction TB

        subgraph FrontLayer["🌐 Capa Frontend"]
            SWA1[swa-web-admin-prd\nAzure Static Web Apps]
            SWA2[swa-web-landing-prd\nAzure Static Web Apps]
        end

        subgraph ComputeLayer["⚙️ Capa de Cómputo — Azure Container Apps Env"]
            CAE[cae-pachamama-prd-brazilsouth]
            CA1[ca-api-admin-prd\n0.5 vCPU / 1GB]
            CA2[ca-api-sync-prd\n0.5 vCPU / 1GB]
            CA3[ca-api-notif-prd\n0.25 vCPU / 0.5GB]
            CA4[ca-api-trace-prd\n0.5 vCPU / 1GB]
        end

        subgraph ServerlessLayer["⚡ Capa Serverless"]
            F1[func-pachamama-sas-prd\nNode.js]
            F2[func-pachamama-tracesync-prd\nNode.js]
        end

        subgraph DataLayer["🗄️ Capa de Datos"]
            PG[(psql-pachamama-prd\nPostgreSQL Flexible\nD2ds_v4 GP + PostGIS)]
            COSMOS[(cosmos-pachamama-prd\nCosmos DB\nMongoDB API Serverless)]
            REDIS[(redis-pachamama-prd\nAzure Cache for Redis\nC1 Standard)]
        end

        subgraph MessagingLayer["🚌 Mensajería y Archivos"]
            SB[sb-pachamama-prd-brazilsouth\nService Bus Standard]
            BLOB[stpmamaprd001\nBlob Storage LRS]
        end

        subgraph OpsLayer["📊 Gobierno y Observabilidad"]
            KV[kv-pachamama-prd\nKey Vault]
            APPI[appi-pachamama-prd\nApplication Insights]
            LAW[law-pachamama-prd\nLog Analytics]
        end
    end

    WEB --> SWA1
    WEB --> SWA2
    SWA1 -- REST --> CA1
    SWA1 -- Solicita SAS --> F1
    APP -- REST --> CA1
    APP -- REST --> CA2
    APP -- REST --> CA3
    APP -- Solicita SAS --> F1
    F1 -- Genera token --> BLOB
    APP -. PUT/GET SAS .-> BLOB
    SWA1 -. GET SAS .-> BLOB
    CA1 -- Persiste op --> PG
    CA1 -- Caché/OTP --> REDIS
    CA2 -- Persiste async --> PG
    CA2 -- pub activities --> SB
    CA3 -- Persiste events --> COSMOS
    CA4 -- ReadModel --> COSMOS
    CA1 -- pub brigade --> SB
    CA1 -- pub traceability --> SB
    CA3 -- sub send-notifications --> SB
    F2 -- sub traceability-events --> SB
    F2 -- Sync ReadModel --> COSMOS
    CA1 -- Validación Token --> FIREBASE
    CA1 -- OTP --> TWILIO
    CA3 -- Push --> FIREBASE
    CA1 -- DNI/RUC --> PERUDEV
    KV -. Secrets .-> CA1
    KV -. Secrets .-> CA2
    KV -. Secrets .-> CA3
    KV -. Secrets .-> CA4
    KV -. Secrets .-> F1
    KV -. Secrets .-> F2
    CA1 -. Telemetría .-> APPI
    CA2 -. Telemetría .-> APPI
    CA3 -. Telemetría .-> APPI
    CA4 -. Telemetría .-> APPI
    APPI --> LAW
```

---

## Opciones de Estrategia de Migración

> Las tres opciones apuntan a la **misma arquitectura objetivo** (diagrama anterior). Se diferencian en cómo se ejecuta la transición para minimizar el impacto al negocio.

---

## Opción A — Migración por Olas (Waves) ⭐ Recomendada

> **Perfil**: Mínimo impacto. Cada "ola" migra un grupo de servicios relacionados, validando en producción antes de avanzar. Ventanas de corte pequeñas (~30 min por ola). Período de costos dobles: ~6–8 semanas.

### Estructura de Olas

```
Wave 1 (Sem 1–2): Fundación + Frontend (cero riesgo de datos)
Wave 2 (Sem 3–5): Bases de Datos (dual-write, sin corte de servicio)
Wave 3 (Sem 6–8): APIs Java → Container Apps (traffic shifting gradual)
Wave 4 (Sem 9):   Cutover final + descomisión proveedores legacy
```

### Diagrama de Flujo de Olas

```mermaid
flowchart TD
    W1["🌊 Wave 1\nFundación + Static Web Apps\nSin toque a datos ni APIs"] 
    W2["🌊 Wave 2\nBases de Datos\nDual-write / Read Replica\nCero downtime"]
    W3["🌊 Wave 3\nAPIs Java → Container Apps\nTraffic split 10% → 100%"]
    W4["🌊 Wave 4\nCutover Final\nDescomisión legacy"]
    
    W1 --> |Validación OK| W2
    W2 --> |Validación OK| W3
    W3 --> |Validación OK| W4
    
    W1 -. rollback trivial .-> W1
    W2 -. apuntar de vuelta a legacy DB .-> W1
    W3 -. revertir DNS/variables .-> W2
```

### Pros y Contras — Opción A

| Pros ✅ | Contras ❌ |
|---------|----------|
| Menor riesgo operativo — rollback disponible en cada ola | Mayor tiempo total de migración (~9–10 semanas) |
| Validación en producción real antes de comprometer cada capa | ~6–8 semanas de costos dobles (legacy + Azure) |
| Equipo puede aprender Azure progresivamente | Requiere más coordinación entre waves |
| Cada wave es una ventana de corte de ~30 min (horario no pico) | |
| Ideal para equipo pequeño (1–2 personas) sin DevOps dedicado | |

**Complejidad Operacional**: Media  
**Time-to-Market**: 9–10 semanas  
**Período de costos dobles**: 6–8 semanas (~USD 150–250 adicionales total)  
**Recomendado para**: Equipo pequeño, primera migración cloud a gran escala, MVP en producción activa

---

## Opción B — Migración por Dominio de Negocio

> **Perfil**: Migrar un dominio completo (servicio + sus datos) de extremo a extremo antes de pasar al siguiente. Reduce el tiempo de costos dobles por dominio, pero requiere coordinación más compleja.

### Estructura por Dominio

```
Dominio 1 (Sem 1–3): Identidad + Fundación + Static Web Apps + API Admin + PostgreSQL
Dominio 2 (Sem 4–5): Sincronización (API Sync + Service Bus + Redis)
Dominio 3 (Sem 6–7): Notificaciones (API Notif + Cosmos DB + FCM routing)
Dominio 4 (Sem 8–9): Trazabilidad (API Trace + Func Trace + Cosmos DB Readmodel)
```

### Pros y Contras — Opción B

| Pros ✅ | Contras ❌ |
|---------|----------|
| Cada dominio queda 100% en Azure antes de avanzar | La API Admin depende de PostgreSQL → la primera wave ya es compleja |
| Tiempo total similar a Opción A pero menor overlap de costos dobles | Las APIs tienen dependencias cruzadas (Admin ↔ Sync ↔ Notifications) |
| Buenos límites para hacer pruebas de integración por dominio | Si falla la migración del Dominio 1, todo queda bloqueado |
| Permite asignar un developer por dominio en paralelo si hay equipo | Requiere manejo cuidadoso de schema de BD durante transición |

**Complejidad Operacional**: Alta  
**Time-to-Market**: 8–9 semanas  
**Período de costos dobles**: 4–6 semanas (solapamiento parcial)  
**Recomendado para**: Equipos con 2+ developers y experiencia en migraciones de BD

---

## Opción C — Migración Acelerada (Big Bang Controlado)

> **Perfil**: Migrar todo en 3–4 semanas con un plan de rollback documentado. Menor tiempo de costos dobles, mayor riesgo. Requiere fin de semana de mantenimiento programado.

### Estructura

```
Semana 1: Provisionar toda la infraestructura Azure + CI/CD
Semana 2: Migración de datos (PostgreSQL, MongoDB, Redis) en paralelo
Semana 3: Desplegar y validar todas las APIs en Container Apps (staging)
Fin de Semana 4: Corte total (ventana de 4–6 horas, comunicado a usuarios)
```

### Pros y Contras — Opción C

| Pros ✅ | Contras ❌ |
|---------|----------|
| Menor período de costos dobles (~3 semanas) | **Mayor riesgo** — un fallo afecta todos los servicios simultáneamente |
| Equipo enfocado en un sprint corto intenso | Requiere ventana de mantenimiento anunciada (4–6 horas de indisponibilidad) |
| Arquitectura Azure operativa en ~4 semanas | Se necesita un plan de rollback muy bien documentado y probado |
| Total de coordinación menor que Opciones A y B | Presión alta sobre el equipo técnico durante el sprint |

**Complejidad Operacional**: Alta  
**Time-to-Market**: 3–4 semanas  
**Período de costos dobles**: ~3 semanas  
**Recomendado para**: Equipos con DevOps dedicado, experiencia en migraciones cloud, o cuando hay presión de presupuesto para reducir costos dobles

---

## Tabla Comparativa de Estrategias

| Criterio | Opción A — Waves ⭐ | Opción B — Dominios | Opción C — Big Bang |
|----------|---------------------|---------------------|---------------------|
| **Duración Total** | 9–10 semanas | 8–9 semanas | 3–4 semanas |
| **Costos Dobles (semanas)** | 6–8 sem | 4–6 sem | ~3 sem |
| **Riesgo de Impacto** | Bajo | Medio | Alto |
| **Rollback** | Por ola, simple | Por dominio, complejo | Total, muy complejo |
| **Tamaño Equipo Recomendado** | 1–2 personas | 2–3 personas | 2–3 + soporte DevOps |
| **Downtime Planificado** | ~30 min × ola | ~1h × dominio | ~4–6h total |
| **Complejidad Coordinación** | Baja | Media | Alta |
| **Experiencia Azure Requerida** | Básica | Intermedia | Avanzada |
| **Arquitectura objetivo** | Idéntica | Idéntica | Idéntica |
| **Costo Mensual Post-Migración** | ~USD 334.94 | ~USD 334.94 | ~USD 334.94 |

---

## Desglose de Servicios y Costos (Arquitectura Objetivo)

> Basado en el consolidado verificado con Azure Retail Prices API — 09 de Abril de 2026.  
> Región: `eastus` (verificación). Despliegue recomendado: `brazilsouth` (~5–10% adicional en Storage).

| # | Recurso Azure | Nombre (CAF) | SKU | Costo/mes (USD) | Justificación |
|---|--------------|-------------|-----|-----------------|---------------|
| 1 | PostgreSQL Flexible — Cómputo | `psql-pachamama-prd` | GP Ddsv5 2 vCore / 8GB · 24/7 | **$129.94** | Reemplaza Railway. Motor relacional principal con PostGIS. Operativo 24/7 = 730 h. ✅ Precio confirmado API |
| 2 | PostgreSQL Flexible — Storage | `psql-pachamama-prd` | Premium SSD 128 GB | **$14.72** | Almacenamiento inicial; escala automáticamente. ⚠️ Precio referencial calculadora |
| 3 | Container Apps — vCPU | `cae-pachamama-prd` | Standard vCPU · 2 vCPU equiv. · 24/7 | **$59.13** | 4 APIs × 0.5 vCPU promedio = 2 vCPU × 730h. Reemplaza 4 Dynos Heroku. ⚠️ Proxy via ACI |
| 4 | Container Apps — Memoria | `cae-pachamama-prd` | Standard Memory · 4 GB · 24/7 | **$12.99** | 4 APIs × 1 GB promedio = 4 GB × 730h. ⚠️ Proxy via ACI |
| 5 | Service Bus — Base | `sb-pachamama-prd` | Standard · Namespace base | **$10.00** | Mensajería asíncrona (queues + topics). ✅ Precio confirmado API |
| 6 | Service Bus — Mensajes | `sb-pachamama-prd` | Standard · ~40M msgs/mes | **$20.00** | Estimado para 1,000 usuarios. ✅ Precio confirmado API |
| 7 | Blob Storage | `stpmamaprd001` | Hot LRS · 200 GB | **$4.16** | Archivos de campo, fotos actividades, onboarding. ✅ Precio confirmado API |
| 8 | Azure Cache for Redis | `redis-pachamama-prd` | C1 Standard · 1 GB · HA | **$55.00** | Reemplaza Redis Labs. Caché OTP + geoespacial. ⚠️ Precio referencial (~$68 máx) |
| 9 | Cosmos DB — Storage | `cosmos-pachamama-prd` | Serverless · 10 GB | **$2.50** | Reemplaza MongoDB Atlas. Colecciones notifications + traceability. ✅ Confirmado |
| 10 | Cosmos DB — RUs | `cosmos-pachamama-prd` | Serverless · ~50M RU/mes | **$12.50** | Estimado para 1,000 usuarios activos. ⚠️ Precio referencial |
| 11 | Static Web Apps | `swa-web-admin-prd` / `swa-web-landing-prd` | Standard · 2 apps | **$9.00** | Reemplaza Vercel. CDN global, custom domains, 100 GB BW incluido. ⚠️ Referencial |
| 12 | Azure Functions | `func-pachamama-sas-prd` / `func-tracesync-prd` | Consumption Y1 | **$5.00** | SAS token gen + ReadModel sync. Tier gratuito 1M exec/mes. ⚠️ Referencial |
| | Key Vault | `kv-pachamama-prd` | Standard | ~$1–3 | Centralización de secretos. No incluido en consolidado. |
| | Application Insights | `appi-pachamama-prd` | Pay-per-use | ~$0–5 | Observabilidad APM. No incluido en consolidado. |
| | Log Analytics | `law-pachamama-prd` | 30 días retención | ~$0–3 | Logs centralizados. No incluido en consolidado. |
| | | | | **TOTAL: ~$334.94 – $350/mes** | |

> **Ahorro potencial con Reserved Instances (1 año)**: PostgreSQL + Redis = ~$184.94/mes  
> Reserva 1 año a PostgreSQL (~30% off) = -$39/mes. Reserva Redis C1 (~20% off) = -$11/mes → **~$50/mes de ahorro en año 2**.

---

## Plan de Implementación por Waves (Opción A Detallada)

### Wave 1 — Fundación, Gobierno y Frontend
**Semanas 1–2 | Riesgo: Muy Bajo | Rollback: Trivial**

Esta ola no toca datos ni APIs. Es completamente reversible en minutos.

| Paso | Actividad | Herramienta | Notas |
|------|-----------|-------------|-------|
| 1.1 | Crear Resource Group `rg-pachamama-prd-brazilsouth` con tags | Azure CLI | `project=pachamama env=prd` |
| 1.2 | Crear Key Vault `kv-pachamama-prd` con RBAC | Azure Portal | Soft-delete ON, purge protection ON |
| 1.3 | Crear Log Analytics `law-pachamama-prd` + Application Insights `appi-pachamama-prd` | Azure Portal | Retención 30 días (free tier) |
| 1.4 | Crear Static Web App `swa-web-admin-prd` desde repositorio GitHub | Azure Portal | Conectar a branch `main` o `prd` |
| 1.5 | Configurar dominio personalizado en `swa-web-admin-prd` → `app.pachamama.eco` | Azure Portal | CNAME switch — downtime ~0 |
| 1.6 | Crear Static Web App `swa-web-landing-prd` | Azure Portal | Conectar a repositorio web-landing |
| 1.7 | Configurar dominio `landing.pachamama.eco` → Static Web Apps | DNS | CNAME switch desde Vercel |
| 1.8 | Configurar alertas de costo: threshold USD 50 y USD 350/mes | Azure Cost Management | Notificación por email |
| 1.9 | Migrar Azure Functions + Storage + Service Bus (Fase 1) | Ver ARQ-FASE1 | Ya documentado en ARQ-FASE1 |

**Definition of Done Wave 1:**
- [ ] Static Web Apps sirviendo correctamente en dominios personalizados
- [ ] Key Vault operativo con al menos 1 secret de prueba
- [ ] ApplicationInsights recibiendo telemetría (aunque sea de test)
- [ ] Alertas de costo configuradas
- [ ] Vercel puede desactivarse sin impacto a producción

---

### Wave 2 — Bases de Datos (Zero Downtime)
**Semanas 3–5 | Riesgo: Medio | Estrategia: Dual-Read**

Esta es la ola más crítica. Se usa una estrategia de **lectura dual** para validar los datos en Azure antes de redirigir el tráfico de escritura.

#### Wave 2A — PostgreSQL (Semana 3)

| Paso | Actividad | Comando / Herramienta | Notas |
|------|-----------|----------------------|-------|
| 2A.1 | Crear servidor `psql-pachamama-prd` GP D2ds_v4 en brazilsouth | Azure Portal / CLI | Habilitar PostGIS extension desde el inicio |
| 2A.2 | Crear base de datos `pachamama_db_prd` | psql CLI | Ya previsto en Fase 2 del ROADMAP |
| 2A.3 | Migración inicial con `pg_dump` + `pg_restore` (snapshot) | pg_dump | En horario de baja actividad |
| 2A.4 | Configurar replicación lógica Railway → Azure PostgreSQL (si Railway lo permite) o re-dump diario | pglogical o pg_dump incremental | Para mantener delta sincronizado |
| 2A.5 | Validar integridad: contar registros clave, verificar PostGIS queries | psql | Comparar counts entre Railway y Azure |
| 2A.6 | Guardar connection string en Key Vault | Azure CLI | Secret: `postgres-connection-string-prd` |
| 2A.7 | Actualizar 1 API (admin) con nueva connection string → validar en staging | Heroku Config Vars | Solo staging, no producción aún |

```bash
# Ejemplo migración PostgreSQL
pg_dump --no-owner --no-acl \
  "postgresql://user:pass@railway-host:port/pachamama_db" \
  | psql "postgresql://admin@psql-pachamama-prd.postgres.database.azure.com/pachamama_db_prd?sslmode=require"

# Verificar extensión PostGIS
psql -c "SELECT PostGIS_Version();" "postgresql://...azure..."
```

#### Wave 2B — MongoDB / Cosmos DB (Semana 4)

| Paso | Actividad | Herramienta | Notas |
|------|-----------|-------------|-------|
| 2B.1 | Crear Cosmos DB `cosmos-pachamama-prd` Serverless en brazilsouth | Azure Portal | Habilitar API for MongoDB, version 7.0 |
| 2B.2 | Crear bases de datos: `pachamama_notifications`, `pachamama_traceability_readmodel_prd` | Azure Portal | Crear índices equivalentes a Atlas |
| 2B.3 | Exportar collections desde Atlas con `mongodump` | mongodump | Usar connection string de Atlas |
| 2B.4 | Importar a Cosmos DB con `mongorestore` | mongorestore | Validar aggregation pipelines usados por las APIs |
| 2B.5 | Ejecutar read test de ambas colecciones contra Cosmos DB | Node.js script | Comparar resultados con Atlas |
| 2B.6 | Guardar Cosmos DB connection string en Key Vault | Azure CLI | Secret: `cosmos-connection-string-prd` |

```bash
# Exportar de Atlas
mongodump --uri="mongodb+srv://user:pass@atlas-cluster/pachamama_notifications" \
  --out=/tmp/mongo-backup

# Importar a Cosmos DB (API MongoDB)
mongorestore --uri="mongodb://cosmos-pachamama-prd.mongo.cosmos.azure.com:10255/..." \
  --ssl /tmp/mongo-backup
```

#### Wave 2C — Redis (Semana 5)

| Paso | Actividad | Herramienta | Notas |
|------|-----------|-------------|-------|
| 2C.1 | Crear Azure Cache for Redis `redis-pachamama-prd` C1 Standard | Azure Portal | TLS only, disable non-TLS port |
| 2C.2 | Exportar snapshot RDB de Redis Labs | Redis Labs portal | Export a Azure Blob Storage |
| 2C.3 | Importar snapshot a Azure Cache for Redis | Azure Portal → Import | Solo para datos de sesión persistidos; los OTP expirarán naturalmente |
| 2C.4 | Actualizar variable `REDIS_URL` en API Admin → staging | Heroku Config Vars | Validar OTP flow y caché geoespacial |
| 2C.5 | Guardar connection string en Key Vault | Azure CLI | Secret: `redis-connection-string-prd` |

**Definition of Done Wave 2:**
- [ ] PostgreSQL Azure con datos migrados, PostGIS funcional, conteos de registros matcheando
- [ ] Cosmos DB con collections importadas, queries de lectura validadas
- [ ] Redis Azure operativo, caché de sesión funcionando en staging
- [ ] Todos los connection strings en Key Vault (0 en texto plano)
- [ ] APIs Heroku validadas contra las nuevas BDs en entorno staging

---

### Wave 3 — APIs Java → Azure Container Apps
**Semanas 6–8 | Riesgo: Medio | Estrategia: Traffic Splitting**

#### Preparación (Semana 6)

| Paso | Actividad | Notas |
|------|-----------|-------|
| 3.1 | Crear Container Apps Environment `cae-pachamama-prd-brazilsouth` | Consumption plan, misma región que BDs |
| 3.2 | Crear `Dockerfile` para cada API Java si no existe | Multi-stage build: Maven build → JRE runtime |
| 3.3 | Crear Azure Container Registry `crpachamama` para imágenes privadas | SKU Basic (~$5/mes) |
| 3.4 | Crear GitHub Actions workflow `deploy-<api>-prd.yml` para cada API | Build → Push ACR → Deploy ACA |
| 3.5 | Configurar Managed Identity en cada Container App para acceder a Key Vault | Sin secrets en App Settings |
| 3.6 | Desplegar todas las APIs en Container Apps con App Settings apuntando a BDs Azure | Validar health checks |

```dockerfile
# Ejemplo Dockerfile para API Java (Spring Boot)
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

#### Traffic Splitting Progresivo (Semanas 7–8)

La estrategia es redirigir el tráfico de producción gradualmente hacia Container Apps, con capacidad de revertir en minutos:

| Día | Porcentaje en Azure ACA | Acción si hay errores |
|-----|------------------------|----------------------|
| Día 1 (Sem 7) | 10% API Admin | Revertir variable en DNS/API Gateway |
| Día 3 | 25% API Admin | Si estable, continuar |
| Día 5 | 50% API Admin + 10% API Sync | Monitorear App Insights |
| Día 7 (Sem 8) | 100% API Admin + 50% API Sync | Validar métricas 24h |
| Día 9 | 100% API Sync + 50% API Notif + 50% API Trace | |
| Día 11 | 100% todas las APIs | Heroku en standby |

> **Mecanismo de traffic split**: Actualizar las variables de entorno `API_ADMIN_URL`, `API_SYNC_URL` en la app frontend (Static Web Apps environment variables) para redirigir gradualmente. Alternativamente, usar Azure API Management como gateway si se desea traffic splitting por porcentaje.

**Definition of Done Wave 3:**
- [ ] Las 4 APIs funcionando en Container Apps con 100% del tráfico
- [ ] App Insights mostrando latencia P95 < 80 ms para endpoints críticos
- [ ] Error rate < 0.1% en las últimas 24 horas
- [ ] Heroku dynos en estado `idle` (tráfico cero) durante 24h consecutivas
- [ ] CI/CD pipeline funcionando: push a `main` → build → push ACR → deploy ACA automático

---

### Wave 4 — Cutover Final y Descomisión
**Semana 9 | Riesgo: Bajo (ya validado) | Ventana: 30 min**

| Paso | Actividad | Responsable |
|------|-----------|-------------|
| 4.1 | Confirmar 72h sin errores en Azure (App Insights) | Dev |
| 4.2 | Tomar snapshot final de Railway PostgreSQL | Dev |
| 4.3 | Desactivar dynos Heroku (no eliminar aún) | Dev |
| 4.4 | Escalar Railway a plan mínimo o free (no eliminar aún) | Dev |
| 4.5 | Desactivar proyecto en MongoDB Atlas (no borrar aún) | Dev |
| 4.6 | Comunicar a stakeholders: "Migración completa — nuevo entorno Azure activo" | PM |
| 4.7 | Mantener legacy activo en stand-by 14 días | Dev |
| 4.8 | Día 14: Eliminar recursos legacy (Heroku apps, Railway DB dev, Atlas cluster) | Dev |
| 4.9 | Actualizar documentación MVP-ARCHITECTURE.md | Dev |

**Definition of Done Wave 4 (Migración Completa):**
- [ ] 100% del tráfico en Azure durante ≥ 72 horas sin incidentes P1/P2
- [ ] Legacy providers en stand-by (no eliminados)
- [ ] Costo Azure dentro del rango ~$334–350/mes
- [ ] Documentación actualizada
- [ ] Backup final de todos los datos legacy almacenado en Blob Storage
- [ ] Credenciales de legacy revocadas después del período de stand-by

---

## Roadmap Visual — Plan Completo (Opción A — Waves)

```mermaid
gantt
    title Migración Completa a Azure — Pachamama (Opción A — Waves)
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m

    section Wave 1 — Fundación + Frontend
    Resource Group + Key Vault + AppInsights   :       w1a, 2026-06-01, 3d
    Static Web Apps (Admin + Landing)          :       w1b, 2026-06-04, 4d
    Dominios + Alertas de Costo               :       w1c, 2026-06-08, 2d
    Azure Functions + Storage + Service Bus    :       w1d, 2026-06-05, 5d

    section Wave 2 — Bases de Datos
    PostgreSQL: provision + migración + validar :      w2a, 2026-06-15, 7d
    Cosmos DB: provision + import + validar    :       w2b, 2026-06-20, 5d
    Redis: provision + import + validar        :       w2c, 2026-06-24, 4d
    Staging: APIs contra BDs Azure             :       w2d, 2026-06-28, 3d

    section Wave 3 — APIs → Container Apps
    Dockerfiles + ACR + GitHub Actions         :       w3a, 2026-07-01, 5d
    Deploy APIs en ACA (staging)               :       w3b, 2026-07-06, 3d
    Traffic split 10% → 50%                    :       w3c, 2026-07-09, 5d
    Traffic split 50% → 100%                   :       w3d, 2026-07-14, 5d

    section Wave 4 — Cutover
    Validación 72h — 100% Azure                :       w4a, 2026-07-19, 3d
    Desactivar legacy providers                :       w4b, 2026-07-22, 2d
    Stand-by 14 días                           :       w4c, 2026-07-24, 14d
    Eliminación legacy + documentación         :       w4d, 2026-08-07, 3d
```

---

## Riesgos y Mitigaciones

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|--------|-------|---------|-----------|
| 1 | **Incompatibilidad PostGIS en PostgreSQL Flexible** — alguna extensión PostGIS no disponible en Azure | Baja | Alto | Validar extensiones disponibles en step 2A.1. Azure PG Flexible soporta PostGIS 3.x. Tener Railway como fallback 2 semanas |
| 2 | **Aggregation pipelines incompatibles en Cosmos DB** — operadores MongoDB sin soporte | Media | Alto | Ejecutar script de prueba con todos los `aggregate()` usados antes del cutover. Si alguno falla, reescribir o mantener Atlas para esa colección |
| 3 | **Pérdida de sesiones Redis durante migración** | Baja | Medio | Las sesiones OTP son de vida corta (~10 min); basta esperar que expiren antes del cutover. Los usuarios deberán re-autenticarse una vez |
| 4 | **Container App fría (cold start) degradando latencia** | Media | Medio | Configurar min replicas = 1 en APIs críticas (admin, sync) para eliminar cold starts. +$20/mes aproximado |
| 5 | **Costos superando estimado por tráfico inesperado** | Baja | Medio | Alertas de costo en $250/mes (warning) y $400/mes (crítico). Revisar Service Bus operations y Cosmos DB RUs semanalmente |
| 6 | **CI/CD pipeline roto durante traffic split** | Media | Alto | Mantener deploy manual como fallback. No hacer splits en viernes. Tener rollback documentado (revertir 1 variable de entorno) |
| 7 | **Cuota insuficiente en brazilsouth para Container Apps** | Media | Bloqueante | Solicitar cuota de Container Apps vCPU con 1 semana de anticipación a Wave 3 |
| 8 | **Heroku APIs con variables de entorno hardcodeadas** | Media | Medio | Auditar variables de entorno de cada API Java antes de Wave 3. Catalogar en Key Vault |
| 9 | **Downtime durante CNAME switch de dominios (Wave 1)** | Baja | Bajo | Usar TTL de 60s en DNS 48h antes del switch. El cambio es imperceptible para usuarios |
| 10 | **Recursos legacy con costos acumulándose si no se eliminan** | Media | Medio | Calendar reminder para eliminar legacy en Día 14 post-cutover. Automatizar con Azure Policy si es posible |

---

## Beneficios Post-Migración

| Dimensión | Antes (Multi-cloud) | Después (Azure Nativo) | Mejora |
|-----------|--------------------|-----------------------|--------|
| **Latencia inter-servicio** | 50–200 ms (cross-provider) | < 5 ms (misma VNet) | ~40× mejor |
| **Gestión de secretos** | Variables dispersas en 4 plataformas | Key Vault centralizado | Auditable, rotable |
| **Observabilidad** | Sin panel unificado | App Insights + Log Analytics | Alertas centralizadas |
| **Escalabilidad** | Manual (Heroku dyno count) | KEDA auto-escala | Sin intervención |
| **Seguridad** | Credenciales en múltiples consoles | Managed Identity + RBAC | Zero secrets en código |
| **Facturación** | 5+ facturas distintas | 1 factura Azure | Simplificación |
| **SLA** | Dependiente de 5 proveedores | Azure 99.5–99.95% | SLA único |

---

## Comparativa de Costos: Antes vs. Después

| Proveedor / Servicio | Costo Actual /mes | Costo Azure /mes | Diferencia |
|---------------------|------------------|-----------------|------------|
| Heroku (4 dynos Basic) | ~$80 | $0 (→ ACA) | -$80 |
| Vercel (2 proyectos) | $0 (Free) | $9 (Static Web Apps) | +$9 |
| Railway (PostgreSQL) | ~$5 | $144.66 (Flexible Server) | +$139.66 |
| MongoDB Atlas | ~$0–9 (M0/M10) | $15 (Cosmos DB Serverless) | +$6–15 |
| Redis Labs | ~$0–7 (free/paid) | $55 (C1 Standard) | +$48–55 |
| Azure Personal (actual) | ~$2 | Incluido en total | — |
| **Total estimado actual** | **~$87–103/mes** | **~$334.94/mes** | **+$232–248/mes** |

> **Nota importante**: El incremento de costo se justifica por la transición de un entorno MVP/free-tier a un entorno de **producción real** con SLA, alta disponibilidad de PostgreSQL (servidor dedicado 24/7), Redis replicado y Container Apps con réplicas activas. El mayor componente del costo actual es Heroku (~$80/mes para 4 dynos Basic), reemplazado en Azure por Container Apps con mayor escalabilidad y observabilidad. Los costos de Railway ($5/mes) y Vercel (gratuito) son bajos porque corresponden a tiers con limitaciones significativas de performance y SLA.
>
> Si el equipo quiere reducir costos en la fase de transición, se puede iniciar con PostgreSQL `Burstable B2ms` (~$50/mes) y Redis `C0 Basic` (~$16/mes) hasta confirmar la carga real, subiendo después de 2–3 semanas si es necesario.

---

## Recomendación Final

**Implementar Opción A — Migración por Olas**, comenzando el **1 de Junio de 2026**, con la siguiente prioridad de ejecución:

1. **Wave 1 (1–14 Junio)**: Provisionar la fundación (Key Vault, App Insights, Static Web Apps). Es de cero riesgo y desbloquea la migración del frontend inmediatamente, eliminando la dependencia de Vercel y estableciendo el gobierno de secretos que toda la migración posterior necesita.

2. **Wave 2 (15 Junio – 5 Julio)**: Migrar las bases de datos con estrategia dual-read. Este es el paso más crítico y requiere mayor atención. La recomendación es hacerlo en días hábiles, con Railway/Atlas/Redis en standby durante 2 semanas adicionales como red de seguridad.

3. **Wave 3 (1–26 Julio)**: Las APIs Java en Heroku son los servicios más fáciles de migrar gracias al modelo de containerización — solo requieren Dockerfile + variables de entorno. El traffic splitting progresivo elimina prácticamente todo el riesgo.

4. **Wave 4 (Agosto)**: Cutover final con 14 días de stand-by antes de eliminar recursos legacy.

5. **Costo aumenta ~$232–248/mes** respecto al estado actual. El costo actual de ~$87–103/mes corresponde en gran parte a Heroku ($80/mes), que será reemplazado por Container Apps con mejor escalabilidad y cobertura de observabilidad. Este costo puede optimizarse post-migración con Reserved Instances ahorrando ~$50/mes adicionales en el año 2.

---

## Referencias

| Recurso | URL |
|---------|-----|
| Azure Container Apps — Precios | https://azure.microsoft.com/es-es/pricing/details/container-apps/ |
| Azure PostgreSQL Flexible Server | https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/overview |
| PostGIS en Azure PostgreSQL | https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-extensions |
| Azure Cosmos DB para MongoDB | https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/introduction |
| Migración MongoDB → Cosmos DB | https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/migrate-databricks |
| Azure Cache for Redis — Import/Export | https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-how-to-import-export-data |
| Azure Static Web Apps | https://learn.microsoft.com/en-us/azure/static-web-apps/overview |
| Container Apps — GitHub Actions | https://learn.microsoft.com/en-us/azure/container-apps/github-actions |
| Azure Key Vault References | https://learn.microsoft.com/en-us/azure/app-service/app-service-key-vault-references |
| pg_dump → Azure PostgreSQL | https://learn.microsoft.com/en-us/azure/postgresql/migrate/how-to-migrate-using-dump-and-restore |
| Azure Pricing Calculator | https://azure.microsoft.com/es-es/pricing/calculator/ |
| Consolidado de costos (interno) | [AZURE-COSTOS-CONSOLIDADO-IoT-Telemetria-1000Usuarios_20260409.md](./AZURE-COSTOS-CONSOLIDADO-IoT-Telemetria-1000Usuarios_20260409.md) |
| Documento Fase 1 (Azure Lift & Shift) | [ARQ-PACHAMAMA-AZURE-20260410.md](./ARQ-PACHAMAMA-AZURE-20260410.md) |
| Versión anterior de este documento | [ARQ-PACHAMAMA-AZURE-FULL-20260410.md](./ARQ-PACHAMAMA-AZURE-FULL-20260410.md) |
