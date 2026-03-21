# Pachamama Func: Traceability Sync (MVP / Pre-Producción)

Microservicio de naturaleza Serverless orientado al procesamiento asíncrono de eventos de negocio enfocados en el seguimiento y auditoría medioambiental / operacional (Trazabilidad).

## Características del Servicio

### Stack Tecnológico

- **Plataforma Cloud:** Azure Functions
- **Lenguaje / Entorno:** [Pendiente revisar el repo para constatar si es Node o C#/Java]
- **Modelo de Ejecución:** Service Bus Trigger

## Integraciones del Servicio

Cumple el rol de "Sincronizador / Consolidador" en el patrón CQRS para que las vistas del landing page corran ultra rápido:

- **Mensajería Interna (Service Bus):** Despierta ante la llegada de nuevos eventos en el bus. Es un consumidor de suscripción (`sub:landing-readmodel-sync-dev`) pegado al tópico reactivo `traceability-events-dev`.
- **Base de datos (MongoDB Atlas):** Una vez mapea y transforma la información consumida, la inserta o hace *upsert* en el datastore no-relacional usando la colección `pachamama_traceability_readmodel_dev` donde luego quedará lista para uso exclusivo de la *API de Traceability*).

## Despliegue / Repositorio

- **Repositorio:** `pachamama-func-trace-sync`
- **Alojamiento:** Function App en la suscripción de Azure.
- **CI/CD:** [Pendiente revisión de workflow / pipeline respectivo]