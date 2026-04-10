# Azure — Servicios de Referencia para Arquitectura Cloud

> Referencia principal del skill `arquitecto-cloud`. Cargar cuando el proveedor sea Azure (default).

---

## Capas Arquitectónicas Azure

### 1. Cómputo

| Servicio | Descripción | Cuándo Usar | SKU Clave |
|----------|-------------|-------------|-----------|
| **Azure App Service** | PaaS para web/API | Apps sin contenedores, equipos sin k8s | B1→P3v3 |
| **Azure Container Apps** | Serverless containers con KEDA | Microservicios, escala a cero | Consumption / Dedicated |
| **Azure Kubernetes Service (AKS)** | Kubernetes gestionado | Workloads complejos, control total | System/User node pools |
| **Azure Functions** | Serverless event-driven | Triggers, procesamiento async, escala a cero | Consumption / Premium EP1-EP3 |
| **Azure Container Instances (ACI)** | Contenedores sin orquestación | Jobs, tareas batch, sidecar rápido | Standard vCPU+Memory |
| **Azure Spring Apps** | PaaS para Spring Boot | Apps Java Spring | Standard / Enterprise |
| **Azure Logic Apps** | Workflows sin código | Integraciones, orquestación procesos | Standard / Consumption |

---

### 2. Base de Datos

| Servicio | Tipo | Cuándo Usar | SKU/Tier |
|----------|------|-------------|----------|
| **Azure Database for PostgreSQL Flexible Server** | Relacional | Apps transaccionales, APIs REST | Burstable B1ms → GP D8ds_v5 |
| **Azure SQL Database** | Relacional (MS SQL) | Apps .NET, reporting, BI | Serverless / General Purpose |
| **Azure Cosmos DB** | Multi-model NoSQL | Alta escala, baja latencia, global | Serverless / Provisioned RU/s |
| **Azure Cache for Redis** | Cache en memoria | Sesiones, rate limiting, pub/sub | C0 Basic → P5 Premium |
| **Azure Database for MySQL Flexible** | Relacional | Apps PHP/Laravel/WordPress | Burstable → General Purpose |
| **Azure Table Storage** | NoSQL key-value | Logs, metadata simple, costo bajo | Standard LRS |
| **Azure SQL Managed Instance** | SQL Server completo PaaS | Migración SQL Server on-premise | General Purpose / Business Critical |

---

### 3. Mensajería y Eventos

| Servicio | Descripción | Cuándo Usar |
|----------|-------------|-------------|
| **Azure Service Bus** | Cola y tópicos enterprise | Desacoplamiento microservicios, garantía de entrega |
| **Azure Event Hubs** | Ingesta de eventos masiva | IoT telemetría, streaming, >1M eventos/seg |
| **Azure Event Grid** | Routing de eventos reactivo | Reaccionar a cambios en recursos Azure, webhooks |
| **Azure Queue Storage** | Cola simple de mensajes | Tareas simples, desacoplamiento básico, costo bajo |
| **Azure Notification Hubs** | Push notifications multi-plataforma | Mobile apps, alerts masivos |

---

### 4. Redes y Seguridad

| Servicio | Descripción |
|----------|-------------|
| **Azure Virtual Network (VNet)** | Red privada aislada, subnets, NSGs |
| **Azure API Management (APIM)** | Gateway API con throttling, políticas, portal dev |
| **Azure Front Door** | CDN + load balancer global con WAF |
| **Azure Application Gateway** | Load balancer L7 regional con WAF |
| **Azure Key Vault** | Gestión de secretos, certificados, claves |
| **Azure Active Directory / Entra ID** | Identidad, SSO, OAuth2/OIDC |
| **Azure Private Endpoint** | Acceso privado a servicios PaaS sin internet público |
| **Azure Firewall** | Firewall gestionado para tráfico VNet saliente |

---

### 5. Almacenamiento

| Servicio | Tipo | Usos |
|----------|------|------|
| **Azure Blob Storage** | Objetos | Archivos, backups, media, logs, datasets |
| **Azure Files** | File share SMB/NFS | Compartir archivos entre VMs/containers |
| **Azure Data Lake Storage Gen2** | Big Data | Analytics, ML datasets |
| **Azure Disk Storage** | Bloque | Discos de VMs (Premium SSD, Ultra) |

---

### 6. Observabilidad y Monitoreo

| Servicio | Descripción |
|----------|-------------|
| **Azure Monitor** | Métricas, logs, alertas centralizadas |
| **Application Insights** | APM para aplicaciones (trazas, métricas, excepciones) |
| **Log Analytics Workspace** | Consultas KQL sobre logs de toda la plataforma |
| **Azure Dashboards / Workbooks** | Visualización personalizada de métricas |

---

### 7. DevOps y CI/CD

| Servicio | Descripción |
|----------|-------------|
| **Azure DevOps Pipelines** | CI/CD, boards, repos, artifacts |
| **Azure Container Registry (ACR)** | Registro privado de imágenes Docker |
| **GitHub Actions + Azure** | CI/CD con workflows YAML, integración nativa |
| **Azure Bicep / ARM Templates** | IaC nativo Azure |
| **Terraform on Azure** | IaC multi-cloud con provider AzureRM |

---

### 8. IA / ML

| Servicio | Descripción |
|----------|-------------|
| **Azure OpenAI Service** | GPT-4, DALL-E, Embeddings con seguridad enterprise |
| **Azure AI Services (Cognitive)** | Vision, Speech, Language, Translator |
| **Azure Machine Learning** | Plataforma MLOps end-to-end |
| **Azure AI Search** | Búsqueda cognitiva con vector search |

---

## Patrones Arquitectónicos Azure Recomendados

### Patrón Web App Estándar
```
Internet → Azure Front Door → App Service / Container Apps → PostgreSQL Flexible / SQL DB
                                                           → Redis Cache
                                                           → Blob Storage
                                                           → Key Vault (secretos)
```

### Patrón Microservicios
```
Internet → API Management → Azure Container Apps (microservicios) → Service Bus
                                                                  → Cosmos DB
                                                                  → Azure Cache for Redis
                                                                  → Storage Account
```

### Patrón IoT / Telemetría
```
Dispositivos → Event Hubs → Azure Functions / Stream Analytics → Cosmos DB / Data Lake
                                                               → Power BI (visualización)
                                                               → Alerts via Monitor
```

### Patrón Serverless Event-Driven
```
Trigger (HTTP/Queue/Timer) → Azure Functions → Service Bus → Functions procesadores
                                             → Blob Storage → Functions downstream
                                             → Cosmos DB
```

---

## SLAs de Referencia Azure

| Servicio | SLA |
|----------|-----|
| App Service (Standard+) | 99.95% |
| Azure Functions (Premium) | 99.95% |
| AKS (control plane) | 99.95% |
| PostgreSQL Flexible (HA) | 99.99% |
| Cosmos DB | 99.999% (multi-region writes) |
| Redis Cache (Standard+) | 99.9% |
| Service Bus (Standard+) | 99.9% |
| Storage (RA-GRS) | 99.99% |
| API Management (Standard+) | 99.95% |

---

## Documentación Oficial

- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
- [Azure Pricing Calculator](https://azure.microsoft.com/es-es/pricing/calculator/)
- [Azure Products by Region](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)
- [Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/)
