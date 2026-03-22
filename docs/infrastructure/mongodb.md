# Base de Datos Documental (MongoDB)

Pachamama utiliza **MongoDB Atlas** como motor de almacenamiento NoSQL. Se usa fundamentalmente como una base de datos secundaria y desacoplada del núcleo transaccional, sirviendo arquitecturas orientadas a eventos como historiales de notificaciones y la capa de lectura (Read-Model) del patrón CQRS para la trazabilidad.

## Configuración del Clúster y Cuenta

- **Plataforma:** MongoDB y MongoDB Atlas (Cloud)
- **Cuenta Administradora:** pachamamadev@gmail.com
- **Proyecto (Atlas):** Project 0
- **Nombre del Clúster:** Cluster0
- **Versión MongoDB:** 8.0.20
- **Tipo de Despliegue:** Replica Set (3 Nodos) para alta disponibilidad.
- **Backups:** Inactivos (En este entorno de MVP).

## Integración Cloud

- **Proveedor Subyacente:** Azure
- **Región:** Virginia-East2 (eastus2)
> *Nota Arquitectónica:* La ubicación está en sintonía geográfica con el Blob Storage (eastus) y Redis, manteniendo bajas las latencias para las Azure Functions en la zona Este estadounidense.

## Seguridad y Acceso

- **Usuario de Base de Datos:** pachamamadev_db_user
- **Método de Autenticación:** SCRAM
- **Rol Asignado:** atlasAdmin@admin (Privilegios amplios por ser un ambiente pre-productivo).
- **Control de Red (IP Access List):**
  - Actualmente abierto globalmente 0.0.0.0/0 para facilitar el acceso de Heroku (que posee IPs dinámicas).
  - Incluye IP manual 38.25.63.84/32 añadida en el Auto Setup.

---

## Bases de Datos Alojadas y Uso

La instancia de MongoDB hospeda actualmente las siguientes bases de datos independientes, cada una con un propósito específico dentro de flujos asíncronos:

### 1. pachamama_notifications
- **Responsabilidad:** Almacenamiento del historial ("bandeja de entrada") de notificaciones de los usuarios. Actualmente utilizado para trazabilizar alertas de tipo "asignación de brigada".
- **Productores / Consumidores:**
  - El microservicio **pachamama-api-notifications-java** escribe y lee de aquí tras consumir eventos originados en el Service Bus.

### 2. pachamama_traceability_readmodel_dev
- **Responsabilidad:** Base de datos que implementa la **capa paralela de lectura rápida (ReadModel)** del arquitectónico CQRS. Aquí habitan los resúmenes denormalizados pre-calculados a partir de eventos transaccionales, diseñados para inyectar la información rápidamente a la Web Landing pública sin tocar el Relacional (PostgreSQL).
- **Productores:** Exclusivamente la función **pachamama-func-trace-sync**.
- **Consumidores:** Consultada de forma ágil desde el API de lectura **pachamama-api-trace-java**.

---

## Próximos Pasos (Migración y Mejora)

1. **Restricción de Tráfico (IP Whitelisting / Peering):** Al estabilizar IPs en un despliegue de Azure futuro (ej. migrando Heroku a Azure App Services con VNet Integration o NAT Gateway), se debe remover la regla 0.0.0.0/0 y configurar Private Endpoints mediante *Azure Private Link* con Atlas.
2. **Backups:** Habilitar rutinas automáticas de *Cloud Backups* de Atlas Atlas una vez el sistema maneje información productiva crítica.
3. **Roles Least Privilege:** Reducir los permisos de pachamamadev_db_user y fragmentarlo en usuarios de base de datos individuales para cada microservicio: un usuario para notifications y un usuario *readonly* y otro *writeonly* para la base de trazabilidad.
