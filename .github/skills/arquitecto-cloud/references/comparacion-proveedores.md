# Comparación de Proveedores Cloud

> Referencia del skill `arquitecto-cloud`. Cargar cuando el usuario solicite escenarios multi-cloud, comparaciones, o mencione explícitamente AWS o GCP.

---

## Equivalencias de Servicios: Azure · AWS · GCP

### Cómputo

| Categoría | Azure | AWS | GCP |
|-----------|-------|-----|-----|
| PaaS Web/API | App Service | Elastic Beanstalk / App Runner | App Engine / Cloud Run |
| Serverless Containers | Container Apps | ECS Fargate / App Runner | Cloud Run |
| Kubernetes | AKS | EKS | GKE |
| Serverless Functions | Azure Functions | AWS Lambda | Cloud Functions |
| VMs | Azure Virtual Machines | EC2 | Compute Engine |
| Batch Jobs | Azure Batch / Container Instances | AWS Batch / ECS | Cloud Batch / Cloud Run Jobs |

### Base de Datos

| Categoría | Azure | AWS | GCP |
|-----------|-------|-----|-----|
| PostgreSQL gestionado | PostgreSQL Flexible Server | Amazon RDS for PostgreSQL / Aurora PostgreSQL | Cloud SQL for PostgreSQL / AlloyDB |
| MySQL gestionado | MySQL Flexible Server | RDS for MySQL / Aurora MySQL | Cloud SQL for MySQL |
| SQL Server | Azure SQL DB / SQL MI | RDS for SQL Server | — (Cloud SQL) |
| NoSQL document | Cosmos DB | DynamoDB / DocumentDB | Firestore / Datastore |
| NoSQL wide-column | Cosmos DB (Cassandra API) | DynamoDB / Keyspaces | Bigtable |
| Cache en memoria | Azure Cache for Redis | ElastiCache (Redis/Memcached) | Memorystore |
| Data Warehouse | Azure Synapse Analytics | Amazon Redshift | BigQuery |
| Time-series | Cosmos DB / Azure Data Explorer | Timestream | BigQuery / InfluxDB on GCP |

### Mensajería y Streaming

| Categoría | Azure | AWS | GCP |
|-----------|-------|-----|-----|
| Cola de mensajes | Service Bus / Queue Storage | SQS | Cloud Pub/Sub / Cloud Tasks |
| Pub/Sub enterprise | Service Bus Topics | SNS | Cloud Pub/Sub |
| Streaming masivo | Event Hubs | Amazon Kinesis | Cloud Pub/Sub / Dataflow |
| Eventos serverless | Event Grid | EventBridge | Eventarc |

### Almacenamiento

| Categoría | Azure | AWS | GCP |
|-----------|-------|-----|-----|
| Object Storage | Blob Storage | S3 | Cloud Storage |
| File Storage | Azure Files | EFS / FSx | Filestore |
| CDN | Azure Front Door / CDN | CloudFront | Cloud CDN |
| Data Lake | ADLS Gen2 | S3 + Lake Formation | Cloud Storage + Dataplex |

### Redes y Seguridad

| Categoría | Azure | AWS | GCP |
|-----------|-------|-----|-----|
| Red privada | VNet | VPC | VPC |
| API Gateway | API Management | API Gateway / AWS AppSync | Apigee / Cloud Endpoints |
| Load Balancer L7 | Application Gateway / Front Door | ALB / CloudFront | Cloud Load Balancing |
| DNS | Azure DNS | Route 53 | Cloud DNS |
| Secretos | Key Vault | AWS Secrets Manager / Parameter Store | Secret Manager |
| Identidad (IdP) | Entra ID / Azure AD | AWS IAM Identity Center / Cognito | Google Cloud Identity / Firebase Auth |
| WAF | Application Gateway WAF / Front Door WAF | AWS WAF | Cloud Armor |

### Observabilidad

| Categoría | Azure | AWS | GCP |
|-----------|-------|-----|-----|
| Monitoreo | Azure Monitor | CloudWatch | Cloud Monitoring |
| APM / Trazas | Application Insights | X-Ray / CloudWatch Application Signals | Cloud Trace / GCP Ops Suite |
| Logs centralizados | Log Analytics (KQL) | CloudWatch Logs / OpenSearch | Cloud Logging |
| Dashboards | Azure Workbooks / Grafana | CloudWatch Dashboards / Grafana | Cloud Dashboards / Grafana |

---

## Cuándo Elegir Cada Proveedor

### Elegir Azure cuando:
- El cliente ya tiene licencias Microsoft (Office 365, Windows Server, SQL Server).
- Requisito de cumplimiento con Microsoft 365 / Active Directory / Entra ID.
- Workloads .NET, C#, o Java empresarial.
- Necesidad de Azure OpenAI Service (GPT-4 enterprise con data privacy).
- Presencia en LATAM con regiones en Brazil South / Mexico Central.
- Integración con GitHub Actions o Azure DevOps.

### Elegir AWS cuando:
- Mayor catálogo de servicios y madurez (150+ servicios).
- Workloads big data y ML/AI con SageMaker.
- Ecosistema open-source más amplio (EKS, Lambda layers).
- Gaming (GameLift), IoT (IoT Core), o media processing.
- El equipo tiene experiencia AWS consolidada.
- Requisito de máxima disponibilidad de zonas (más AZs por región que Azure).

### Elegir GCP cuando:
- Big data y analytics masivo (BigQuery es best-in-class).
- Machine Learning avanzado (Vertex AI, TPUs).
- Kubernetes (GKE es el Kubernetes más maduro por ser Google quien lo creó).
- Aplicaciones mobile con Firebase como backend.
- Workloads de búsqueda o procesamiento de datos a escala web.
- Startups con créditos Google for Startups.

---

## Regiones Clave por Proveedor

### Azure — Regiones LATAM
| Región | Localidad | Zona Disponible |
|--------|-----------|-----------------|
| Brazil South | São Paulo, Brasil | ✅ |
| Brazil Southeast | Rio de Janeiro, Brasil | ✅ |
| Mexico Central | Querétaro, México | ✅ |
| Chile Central | Santiago, Chile | (próximamente) |

### AWS — Regiones LATAM
| Región | Localidad | AZs |
|--------|-----------|-----|
| sa-east-1 | São Paulo, Brasil | 3 |
| us-east-1 | N. Virginia (baja latencia LATAM) | 6 |

### GCP — Regiones LATAM
| Región | Localidad |
|--------|-----------|
| southamerica-east1 | São Paulo, Brasil |
| southamerica-west1 | Santiago, Chile |
| northamerica-northeast1 | Montréal |

---

## AWS — Servicios Clave de Referencia

### Cómputo AWS
- **EC2**: VMs con >600 tipos de instancia. `t3.micro` (free tier) → `m6i.16xlarge`.
- **ECS/Fargate**: Contenedores serverless sin gestión de nodos. Pricing: vCPU+Memory por segundo.
- **EKS**: Kubernetes gestionado. $0.10/hora por cluster control plane.
- **Lambda**: Funciones serverless. 1M req/mes gratis. $0.20/1M req después.
- **App Runner**: PaaS para contenedores. Deploy desde ECR o código fuente.

### Base de Datos AWS
- **RDS**: PostgreSQL, MySQL, SQL Server, Oracle, MariaDB gestionados.
- **Aurora**: MySQL/PostgreSQL compatible, 5x más rápido que RDS estándar. Serverless v2.
- **DynamoDB**: NoSQL key-value/document. On-demand o provisioned. Global Tables.
- **ElastiCache**: Redis (Valkey) o Memcached gestionado.
- **DocumentDB**: MongoDB compatible (atención: no es MongoDB real, sino reimplementación AWS).

### Mensajería AWS
- **SQS**: Cola de mensajes. Standard (best-effort) o FIFO (exactamente una vez).
- **SNS**: Pub/Sub fanout. Integra con SQS, Lambda, HTTP, email.
- **EventBridge**: Bus de eventos serverless. Reglas de routing a +20 targets.
- **Kinesis**: Streaming de datos en tiempo real. Data Streams, Firehose, Analytics.

---

## GCP — Servicios Clave de Referencia

### Cómputo GCP
- **Cloud Run**: Containers serverless, escala a cero. Pay per request. Mejor serverless container experience.
- **GKE**: Kubernetes con autopilot mode (sin gestión de nodos). Estándar de la industria.
- **Cloud Functions Gen2**: Basado en Cloud Run. Mayor tiempo de ejecución (60 min).
- **App Engine**: PaaS original de Google. Standard (escala a cero) y Flexible (containers).
- **Compute Engine**: VMs con Live Migration (VMs no se reinician en mantenimiento).

### Base de Datos GCP
- **Cloud SQL**: PostgreSQL, MySQL, SQL Server gestionados.
- **AlloyDB**: PostgreSQL compatible, 100x más rápido para analytics que Cloud SQL.
- **Firestore**: NoSQL document database, serverless, integración nativa con Firebase.
- **Bigtable**: NoSQL wide-column para IoT, analytics, >10TB. HBase compatible.
- **BigQuery**: Data warehouse serverless. $5/TB consultado. Mejor para analytics.
- **Spanner**: NewSQL distribuido global. SLA 99.999%. Costoso pero único.

---

## Documentación Oficial

- [Azure vs AWS naming guide](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/services)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [GCP Documentation](https://cloud.google.com/docs)
- [Azure Pricing](https://azure.microsoft.com/pricing/calculator/)
- [AWS Pricing Calculator](https://calculator.aws/pricing/2/home)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)
