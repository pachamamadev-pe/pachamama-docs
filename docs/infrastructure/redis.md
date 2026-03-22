# Caché y Estado Volátil (Redis)

Pachamama utiliza **Redis** como motor de almacenamiento de clave-valor en memoria. Su propósito principal es acelerar las lecturas de componentes geoespaciales pesados y manejar tiempos de vida (TTL) de los estados temporales de los usuarios (como códigos de seguridad).

## Configuración y Credenciales

- **Cuenta Propietaria:** pachamamadev@gmail.com
- **Proveedor:** Redis Labs (Hospedado en infraestructura de nube de Azure)
- **Base de Datos (Nombre):** database-MLD6YX0S
- **Región:** East US (Virginia) east-us

## Especificaciones de Conexión

- **Endpoint Público:** edis-11401.c251.east-us-mz.azure.cloud.redislabs.com
- **Puerto:** 11401
- **Versión de Redis:** 8.2
- **Protocolo Soportado:** RESP3

## Capacidades y Gobernanza de Datos (MVP)

La instancia actual opera bajo un perfil de uso inicial sin alta disponibilidad.

- **Almacenamiento Máximo (Dataset Size):** 30 MB *(Uso promedio: ~7 MB)*
- **Límite de Red Mensual:** 5 GB
- **Alta Disponibilidad (HA):** Ninguna (Single Node)
- **Persistencia de Datos:** Ninguna (Los datos viven netamente en RAM)
- **Política de Evicción:** olatile-lru *(Cuando el límite de 30 MB se llena, elimina las claves con expiración (TTL) que se hayan utilizado menos recientemente).*

---

## Casos de Uso Activos

El ecosistema hace uso de Redis para resolver tres grandes necesidades, controladas principalmente desde pachamama-api-admin-java:

### 1. Gestión de Códigos de Onboarding
Cuando un nuevo recolector es registrado, el sistema genera códigos temporales de habilitación. Estos se persisten en caché en lugar de la base de datos central:
- **Expiración Estándar:** 7 días (configurable mediante parámetros de la API).

### 2. Control y Rate-Limiting de OTP (One Time Password)
Se controlan los intentos de un usuario para proteger el uso indiscriminado de envíos de SMS por validaciones:
- Claves de control de intentos: otp:verify_attempts:<phone/id>.
- Claves de trazabilidad de tiempo de vida: otp:created:<phone/id>.

### 3. Caché Geoespacial de Dashboard (GeoJSON)
Una de las consultas más pesadas es dibujar las "Zonas Operativas" en el App/Web, ya que requiere agrupar todos los mapas y polígonos de todos los proyectos de una empresa.
- **Implementación:** El resultado se procesa una vez en PostgreSQL/PostGIS y se almacena en caché en la clave geojson:company:<id_empresa>. Las subsiguientes peticiones leen la estructura de datos espaciales directamente desde Redis a altísima velocidad.

---

## Próximos Pasos (Migración y Escala)

- Dado que la región elegida subyacente es **East US en Azure**, esta decisión está perfectamente alineada con el Blob Storage actual (eastus).
- Al evolucionar a un escenario productivo, la migración natural es transaccionar desde *Redis Labs Cloud* hacia el servicio nativo supervisado **Azure Cache for Redis** en el mismo tenant de Azure (codeoncube.onmicrosoft.com). Hacer eso no requerirá cambiar la lógica de las APIs, pero dotará de Alta Disponibilidad (Replicación Primario/Secundario), integración dentro de una misma *VNet* (red virtual) para evitar latencia de red pública y persistencia RDB en disco.
