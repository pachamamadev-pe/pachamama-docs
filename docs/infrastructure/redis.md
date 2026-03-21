# Caché Redis (MVP / Pre-Producción)

Redis está presente en la arquitectura para optimizar la carga y la latencia en consultas repetitivas inter-bancarias hacia el core relacional.

## Cuentas y Proveedor Cloud

- **Proveedor Cloud Actual:** `[Pendiente de definir ej. Add-on de Heroku, Upstash, propio]`
- **Cuenta Administradora:** `[Pendiente de definir]`

## Integraciones y Configuraciones Cloud

### Servicio Conectado (`DBR`)
- El motor de redis está intrínsecamente validado contra `pachamama-api-admin-java`. Su meta es descargar la persistencia operativa usando estrategias de Cache-Aside sobre catálogos y resultados pesados para acelerar las respuestas al frontend.