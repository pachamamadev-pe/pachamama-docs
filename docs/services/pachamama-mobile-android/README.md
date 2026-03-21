# Pachamama Mobile App (MVP / Pre-Producción)

Aplicación móvil principal que utilizan los recolectores de campo y brigadistas. Su factor clave es la capacidad de **operar en entornos sin conectividad (offline-first)**, guardando el trabajo localmente y encolando la sincronización para el momento en el que el dispositivo recupere conexión a Internet.

## Características del Servicio

### Stack Tecnológico

- **Plataforma:** Android
- **Lenguaje:** [Pendiente de perfilar, e.g. Kotlin]
- **Arquitectura Local:** [Pendiente de definir, e.g. MVVM / Room para persistencia local]

## Integraciones del Servicio

La aplicación móvil es el cliente más robusto del sistema y se integra de la siguiente manera:

- **Identidad (Firebase Auth):** Usa el SDK nativo de Firebase para que los recolectores inicien sesión en el sistema usando su teléfono (validación SMS/OTP).
- **Backend Operativo (`pachamama-api-admin-java`):** Lee configuraciones, perfiles, formularios dinámicos y brigadas asignadas bajo una conexión REST clásica.
- **Backend Sincronización (`pachamama-api-sync-java`):** Punto clave; envía todos los eventos recopilados offline hacia este microservicio en paquetes.
- **Gestión de Archivos (Azure):** 
    1. Invoca a `pachamama-func-sas-node` vía REST para solicitar un token de seguridad temporal con permisos (Lectura/Escritura).
    2. Usa el SAS Token para comunicarse directamente de forma subyacente para subir multimedia (fotos de campo, documentos) al `Azure Blob Storage`.
- **Notificaciones (FCM):** Recibe Push Notifications del sistema emitidas a su token de dispositivo.

## Distribución / Repositorio

- **Repositorio:** `pachamama-mobile-android`
- **Integración/Despliegues:** [Pendiente de definir, e.g. AppTester / Firebase App Distribution / Play Store]
