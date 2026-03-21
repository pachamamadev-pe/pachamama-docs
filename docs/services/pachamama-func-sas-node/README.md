# Pachamama Func: SAS Generator (MVP / Pre-Producción)

Microservicio en formato Serverless (Azure Functions) encargado de emitir firmas de acceso compartido o *Shared Access Signatures (SAS Tokens)*. 

## Características del Servicio

### Stack Tecnológico

- **Plataforma:** Azure Functions
- **Lenguaje / Entorno:** Node.js
- **Modelos de Ejecución:** HTTP Trigger

## Integraciones del Servicio

Su objetivo es proveer seguridad de acceso al almacenamiento sin exponer la cadena (connection string) real de la cuenta de Azure. 

- **Consumidores Frontend:** Son llamados vía REST HTTP por ambos el `pachamama-mobile-android` y el `pachamama-web-admin` cuando uno de ellos tiene intención de cargar una fotografía/documento, o bien acceder a uno privado para visualizarlo.
- **Autorizador / Cloud:** Se conecta subyacentemente usando librerías y secreto maestro a la cuenta protegida de **Azure Blob Storage** para expedir tokens con un nivel de permiso (read / write) y tiempo de caducidad super específicos que luego devuelve al frontend.

## Despliegue / Repositorio

- **Repositorio:** `pachamama-func-sas-node`
- **Alojamiento:** Function App en la suscripción de Azure.
- **CI/CD:** [Pendiente revisar el pipeline o GitHub action utilizado para el empaquetado y subida a la Function].
