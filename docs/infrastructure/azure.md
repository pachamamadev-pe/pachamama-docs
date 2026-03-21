# Plataforma Azure (MVP / Pre-Producción)

La infraestructura cloud de **Microsoft Azure** hospeda los servicios asíncronos, almacenamiento de objetos y plataforma serverless de la arquitectura.

## Cuentas

- **Cuenta Principal / Suscripción:** `[Pendiente de definir]`
- **Uso:** Alojamiento de colas y tópicos, funciones serverless y blob storage.

## Integraciones y Configuraciones Cloud

### Recursos Configurados

- **Azure Functions (Serverless):**
    - `pachamama-func-sas-node`: Función encargada de validar usuarios y generar los tokens SAS (Shared Access Signature) de lectura o escritura al vuelo.
    - `pachamama-func-trace-sync`: Función consumidora para sincronizar y consolidar la información en el entorno de solo-lectura (ReadModel) para la landing page.
- **Azure Blob Storage:**
    - **Cuenta de Storage:** `sapachamama001`
    - **Propósito:** Almacenamiento seguro de archivos subidos por el Admin (`admin-uploads`) o desde la App móvil. Todo el acceso es gobernado mediante URLs con tokens SAS.
- **Azure Service Bus (Mensajería):**
    - **Namespace:** `pachamama-sync-batch`
    - **Cola (`activities-sync-queue`):** Usada por la API Sync para encolar trabajo offline.
    - **Tópicos:**
      - `assigned-brigade`: Para emisión de eventos a la API de Notificaciones.
      - `traceability-events-dev`: Para procesar eventos hacia la función consolidadora de trazabilidad.
