# Integraciones PaaS y Servicios Complementarios

> Referencia del skill `arquitecto-cloud`. Cargar cuando el usuario mencione Firebase, Heroku, Railway, MongoDB Atlas, Supabase, Vercel, Netlify, Render, Neon, PlanetScale, Upstash, u otros servicios BaaS/PaaS complementarios.

---

## Firebase (Google BaaS)

### ¿Cuándo integrar Firebase?
- Apps mobile (Android/iOS) que necesitan auth, base de datos en tiempo real o push notifications.
- Prototipos rápidos y MVPs que no requieren backend propio.
- Complemento para autenticación en arquitecturas GCP o Azure.
- Apps con requisito de sync offline (Firestore offline support).

### Servicios Firebase

| Servicio | Descripción | Integración con Cloud |
|----------|-------------|----------------------|
| **Firebase Authentication** | Auth social (Google, Facebook, Apple, GitHub, Email) + JWT | Cualquier backend puede validar JWT Firebase. Integra con Azure API Management, AWS Cognito como IdP externo. |
| **Firestore** | NoSQL document database, realtime listeners | Puede usarse como capa de datos frontend; backend en Azure/AWS accede vía Admin SDK. |
| **Realtime Database** | JSON tree sincronizado en tiempo real | Ideal para chats, cursores colaborativos, dashboards live. |
| **Firebase Storage** | Object storage basado en Google Cloud Storage | Subida de archivos desde cliente. Backend puede usar GCS directamente. |
| **Firebase Cloud Messaging (FCM)** | Push notifications cross-platform | Backend envía via FCM API. Integra con Azure Notification Hubs o AWS SNS. |
| **Firebase Hosting** | Hosting de SPAs y sites estáticos con CDN | Alternativa a Azure Static Web Apps o AWS S3+CloudFront para frontend. |
| **Firebase Remote Config** | Feature flags y configuración remota | Complementa cualquier arquitectura de feature flags. |
| **Firebase App Check** | Verificación de autenticidad de llamadas de apps móviles | Seguridad adicional para APIs backend. |

### Patrón de Integración Firebase + Azure
```
Mobile App → Firebase Auth (JWT) → Azure API Management (validar JWT) → Azure Container Apps (backend)
           → Firestore (datos en tiempo real)                           → PostgreSQL (datos transaccionales)
           → FCM (push)                                                 → Service Bus (mensajería interna)
```

---

## Heroku (Salesforce PaaS)

### ¿Cuándo usar Heroku?
- **Dev/Staging**: Entorno temporal de desarrollo o QA, despliegue rápido con `git push heroku`.
- **Startups tempranas**: Sin equipo DevOps, necesitan deployar en minutos.
- **Aplicaciones Ruby on Rails, Node.js, Python** con addons gestionados.
- Proyectos pequeños donde el equipo no quiere operar infraestructura.

### Componentes Heroku

| Componente | Descripción | Azure Equivalente |
|------------|-------------|-------------------|
| **Dynos** | Contenedores de aplicación | App Service / Container Apps |
| **Heroku Postgres** | PostgreSQL gestionado (powered by AWS RDS) | PostgreSQL Flexible Server |
| **Heroku Redis** | Redis gestionado | Azure Cache for Redis |
| **Heroku Data for Apache Kafka** | Managed Kafka | Azure Event Hubs (Kafka protocol) |
| **Heroku Pipelines** | CI/CD y promotion entre entornos | Azure DevOps / GitHub Actions |
| **Heroku Connect** | Sync con Salesforce | Power Automate / Salesforce connector |

### Limitaciones Heroku para Producción
- Sin zonas de disponibilidad propias (corre sobre AWS us-east-1).
- Pricing elevado para escala media/alta vs. Azure/AWS directo.
- Vendor lock-in en addons Heroku.
- **Recomendación**: Usar para dev/staging, migrar a Azure/AWS en producción.

---

## Railway

### ¿Cuándo usar Railway?
- **Dev/Staging** con despliegue desde GitHub en segundos.
- Equipos pequeños sin DevOps que necesitan contenedores, bases de datos y workers.
- Proyectos con stacks modernos (Next.js, FastAPI, Go, Rust, etc.).
- Alternativa a Heroku más económica para proyectos early-stage.

### Servicios Railway

| Servicio | Descripción | Azure Equivalente |
|----------|-------------|-------------------|
| **Railway Services** | Containers desde Dockerfile o Nixpacks | Container Apps / App Service |
| **Railway PostgreSQL** | PostgreSQL gestionado | PostgreSQL Flexible Server |
| **Railway MySQL** | MySQL gestionado | MySQL Flexible Server |
| **Railway Redis** | Redis gestionado | Azure Cache for Redis |
| **Railway MongoDB** | MongoDB gestionado | Cosmos DB (MongoDB API) |
| **Private Networking** | Red privada entre servicios del proyecto | VNet / Private Endpoints |
| **Volumes** | Persistent storage para containers | Azure Managed Disks / Files |

### Railway vs. Heroku vs. Azure (Decisión Rápida)

| Criterio | Railway | Heroku | Azure Container Apps |
|----------|---------|--------|---------------------|
| Precio entrada | $5/mes (Hobby) | $5-7/dyno | Pay-per-use, ~$0 idle |
| Facilidad deploy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Escalabilidad | Media | Media | Alta |
| Producción enterprise | ❌ | ❌ | ✅ |
| SLA | ~99.9% (no garantizado) | ~99.9% | 99.95% |
| LATAM región | ❌ (sin región SA) | ❌ | ✅ (Brazil South) |

---

## MongoDB Atlas

### ¿Cuándo integrar MongoDB Atlas?
- El stack ya usa MongoDB y se quiere evitar migración.
- Documentos JSON sin esquema fijo, necesidad de cambios de estructura frecuentes.
- Operaciones geoespaciales, full-text search (Atlas Search integrado).
- Multi-cloud: Atlas puede correr en Azure, AWS o GCP con el mismo proveedor.
- Aplicaciones MEAN/MERN stack.

### Integración MongoDB Atlas con Azure

| Patrón | Descripción |
|--------|-------------|
| **Atlas on Azure** | Cluster MongoDB Atlas desplegado en region Azure (ej: East US) |
| **Private Endpoint** | Conexión privada entre VNet Azure y Atlas vía Private Link |
| **Atlas Data Federation** | Query sobre Blob Storage + Atlas desde una sola interfaz |
| **Atlas Search** | Elasticsearch-compatible search sobre documentos MongoDB |
| **Atlas App Services** | Backend lógico serverless (triggers, funciones) similar a Firebase |
| **Atlas Vector Search** | Búsqueda semántica por embeddings vectoriales |
| **Atlas Stream Processing** | Procesamiento de eventos en tiempo real |

### Configuración VNet Peering Azure + MongoDB Atlas
```
Azure VNet (10.0.0.0/16)
  └── Subnet Apps (10.0.1.0/24)
        └── Container Apps / AKS           ←── Private Link ──→  MongoDB Atlas Cluster
                                                                   (Azure East US)
```

---

## Supabase (Open-source Firebase alternative)

### ¿Cuándo integrar Supabase?
- Alternativa open-source a Firebase, basada en PostgreSQL real.
- Necesidad de PostgreSQL con Auth, Storage y Realtime en un solo servicio.
- Proyectos que quieren auto-hosting o no depender de Google.
- Frontend-heavy apps (React, Next.js, Vue) con acceso directo a DB desde cliente.

### Servicios Supabase

| Servicio | Equivalente Azure |
|----------|------------------|
| Supabase Auth | Entra ID External Identities / Firebase Auth |
| Supabase Database (PostgreSQL) | Azure Database for PostgreSQL |
| Supabase Realtime | Azure Web PubSub / SignalR Service |
| Supabase Storage | Azure Blob Storage |
| Supabase Edge Functions | Azure Functions (Deno runtime) |
| Supabase Vector | Azure AI Search (vector) |

---

## Vercel / Netlify (Frontend Hosting)

| Servicio | Descripción | Azure Equivalente |
|----------|-------------|-------------------|
| **Vercel** | Deploy de Next.js/React con Edge Network global | Azure Static Web Apps (Standard) |
| **Netlify** | JAMstack hosting con Forms, Functions, Identity | Azure Static Web Apps + Functions |

### Integración Vercel + Azure Backend
```
Vercel (Frontend Next.js)  →  HTTPS  →  Azure API Management  →  Azure Container Apps (API)
                                                                 →  PostgreSQL Flexible Server
```

---

## Upstash (Serverless Redis y Kafka)

| Servicio | Descripción | Azure Equivalente |
|----------|-------------|-------------------|
| **Upstash Redis** | Redis serverless, pago por req | Azure Cache for Redis (Basic/free tier) |
| **Upstash Kafka** | Kafka serverless | Azure Event Hubs |
| **Upstash Vector** | Vector DB serverless | Azure AI Search |
| **Upstash QStash** | Cola de mensajes HTTP | Azure Service Bus |

**Cuándo usar Upstash sobre Azure Cache**: proyectos pequeños, funciones serverless en Vercel/Netlify que necesitan Redis sin VNet, o cuando el costo fijo de Redis Azure ($16/mes mínimo) es prohibitivo.

---

## Neon (PostgreSQL Serverless)

- PostgreSQL serverless con escala a cero (branching de DB como Git branches).
- Ideal para entornos de testing o proyectos donde la DB esté inactiva gran parte del tiempo.
- **Integración con Vercel**: Neon es el proveedor PostgreSQL nativo de Vercel.
- **Azure equivalente**: PostgreSQL Flexible Server con tier Burstable B1ms (~$14/mes, no escala a cero).

---

## PlanetScale (MySQL Serverless)

- MySQL compatible, branching de schema (deploy requests).
- Basado en Vitess (YouTube's database scaling solution).
- Escala horizontal automática para MySQL.
- **Azure equivalente**: Azure Database for MySQL con sharding manual.

---

## Cloudflare (Edge y Workers)

| Servicio | Descripción | Azure Equivalente |
|----------|-------------|-------------------|
| **Cloudflare Workers** | JS/WASM en el edge (~300 PoPs) | Azure Functions + Front Door |
| **Cloudflare Pages** | Frontend hosting estático | Azure Static Web Apps |
| **Cloudflare D1** | SQLite distribuida en edge | (Sin equivalente directo) |
| **Cloudflare R2** | Object storage sin egress fees | Azure Blob Storage |
| **Cloudflare KV** | Key-Value global en edge | Azure Cache for Redis (global) |
| **Cloudflare Tunnels** | Exponer servicios locales/on-premise | Azure VPN Gateway |

---

## Patrones de Integración Recomendados

### Patrón Startup (Railway + MongoDB Atlas)
```
Dev/Staging: Railway (containers + PostgreSQL)
Production:  Azure Container Apps → MongoDB Atlas (Private Link) → Azure Blob Storage
             Azure API Management (gateway) → Azure Cache for Redis
```

### Patrón Mobile (Firebase Auth + Azure Backend)
```
Mobile App → Firebase Auth → JWT Token → Azure API Management → Azure Container Apps
           → Firebase Realtime DB (sync offline)              → Azure SQL / PostgreSQL
           → FCM Push Notifications                           → Azure Service Bus
```

### Patrón JAMstack (Vercel + Azure)
```
Vercel (Next.js, SSR/SSG) → Azure API Management → Azure Container Apps (API REST)
                          → Azure Static Web Apps (fallback)  → PostgreSQL Flexible Server
                                                              → Azure Cache for Redis
```

### Patrón Datos Universales (Atlas + Azure)
```
Azure Container Apps → MongoDB Atlas (Private Link, Azure region)
                     → Azure Blob Storage (Atlas Data Federation)
                     → Atlas Search (full-text)
                     → Atlas Vector Search (embeddings)
```
