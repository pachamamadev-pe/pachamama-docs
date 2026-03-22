# Firebase (Identidad y Notificaciones)

Pachamama utiliza **Google Firebase** como ecosistema administrado para dos pilares críticos: el control de Identidad/Autenticación de usuarios (Authentication) y la distribución de alertas push a dispositivos (Cloud Messaging).

## Entorno y Proyecto

- **Cuenta Administradora:** pachamamadev@gmail.com
- **Plan de Facturación:** *Spark* (Sin costo - USD 0 al mes)
- **Nombre del Proyecto:** pachamama-mvp
- **ID del Proyecto:** pachamama-mvp
- **Número del Proyecto:** 1091949587458

---

## Aplicaciones Registradas (Apps)

Firebase maneja identidades separadas para las diferentes aplicaciones cliente que se conectan al proyecto unificado.

### 1. Aplicación Móvil (Android)
- **Nombre Interno:** PachamamaApp
- **Paquete:** com.pachamama.mobile
- **App ID:** 1:1091949587458:android:404ed8352f6e9b46080b1b
- **Uso Restringido:** Se utiliza dentro de la app Android de recolección de datos y recibe certificados del tipo google-services.json para autorizar las subscripciones push.

### 2. Aplicación Web (React/Vite)
- **Nombre Interno:** web-app
- **App ID:** 1:1091949587458:web:587f5aa58892fe06080b1b
- **Dominio de Auth:** pachamama-mvp.firebaseapp.com

---

## Servicios Activos

### A. Firebase Authentication
Actúa como IDP (Identity Provider). Los clientes intercambian contraseñas por JWT (*JSON Web Tokens*) que posteriormente el backend de Java verifica interconectándose con las claves públicas provistas por Google.
- **Métodos Habilitados:** Exclusivamente *Correo electrónico / Contraseña*.

### B. Firebase Cloud Messaging (FCM V1)
Utilizado para orquestar la entrega de notificaciones asíncronas (Alertas, avisos de asignación) desencadenadas por la arquitectura guiada por eventos de Pachamama.
- **Versión de API:** V1 (Requerida tras la depreciación de legacy push de Google).
- **ID del Remitente (Sender ID):** 1091949587458
- **Certificados Push Web (VAPID):** BIgXJxrV22yQ3oEp5y-xQQOQHAhzee4tG1qz-QE5... (Clave pública para soporte futuro de web workers).

---

## Integraciones y Migración

> **Nota de Desarrollo:** Ya que usamos la versión gratuita **Spark**, si el proyecto comienza a escalar la autenticación masiva (decenas de miles de SMS-auth o más de 50,000 MAU), la cuenta debe moverse al plan *Blaze* (pago por uso). De momento para un ambiente MVP la capa es lo suficientemente robusta. Si más adelante se plantea integrar SSO (Single Sign-On) como Azure AD (Entra ID), se deberían configurar políticas de Tenant e integraciones Custom Providers dentro de la misma cuenta unificada.
