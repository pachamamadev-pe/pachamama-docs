# Gestión de Cambios: Consentimiento Informado Cifrado y Gestión de Errores

## Registro de Cambios

---

## [30 Mar – 8 Abr 2026] Onboarding con Consentimiento Cifrado y Gestión de Errores en Sincronización

**Autor:** Jecri Do Santos  
**Período:** 30 de Marzo – 8 de Abril 2026 *(10 días)*  
**APK generada:** `v1.2.0`

**Objetivo:** Implementar el flujo de consentimiento informado personalizado y cifrado durante el onboarding del recolector, y consolidar la gestión robusta de errores en la sincronización de actividades con política de reintentos.

### Contexto

Durante el proceso de onboarding, el recolector debe aceptar un documento de consentimiento informado que incluye datos específicos de su identidad y de la empresa cliente. Para garantizar la integridad del contenido recibido:

1. **Cifrado del consentimiento:** El documento es solicitado y recibido con cifrado **RSA-OAEP + AES-256-GCM**, el mismo mecanismo del flujo de envío de onboarding, garantizando que el contenido no sea alterado en tránsito.
2. **Personalización en el servidor:** Los parámetros del documento (`[[NOMBRE_RECOLECTOR]]`, `[[DNI_RECOLECTOR]]`, `[[RAZON_SOCIAL_CLIENTE]]`, etc.) son reemplazados por el backend con datos reales, evitando que el cliente maneje plantillas crudas.
3. **Política de reintentos para sincronización:** Las actividades con 3 o más intentos fallidos son excluidas de las sincronizaciones automáticas futuras para evitar ciclos infinitos.

---

### Componentes Modificados

| Componente | Versión | Descripción del Cambio |
|---|---|---|
| [Pachamama Mobile Android](pachamama-mobile-android.md) | `v1.1.0` → `v1.2.0` | Consentimiento cifrado, gestión de errores en sync, estrategia Online-First |
| [Pachamama API Admin (Java)](pachamama-api-admin-java.md) | — | Nuevo endpoint `POST /legal-documents/encrypted` con resolución de contexto y reemplazo de parámetros |
| [Pachamama API Notifications (Java)](pachamama-api-notifications-java.md) | `v1.3.0` | Nueva API de Event Logging (`events_logging`) con registro y consultas paginadas |

---

### Flujo del Cambio — Consentimiento Informado Cifrado

```
ConsentScreen (Android)
   │  Lee accessCode / accessType desde OnboardingPreferences
   │  Llama a loadInformedConsentEncrypted(accessCode, type, firstName, lastName, dni)
   ▼
ConsentViewModel
   │  Mapea accessType → invitationType ("SHORT_CODE")
   │  Normaliza nombre a mayúsculas (collectorName)
   ▼
OnboardingRepository — getLegalDocumentEncrypted()
   │  Reutiliza getOnboardingPublicKey() (caché de sesión)
   │  Cifra el payload con RSA-OAEP + AES-256-GCM
   ▼
Backend — POST /api/v1/collectors/onboarding/legal-documents/encrypted
   │  Reemplaza parámetros [[...]] con datos reales del recolector y empresa
   │  Devuelve documento personalizado cifrado
   ▼
ConsentScreen
   └─ Renderiza documento Markdown en Dialog (pantalla completa, Markwon)
      Con fallback automático al endpoint GET sin cifrar si el endpoint falla
```

---

### Conclusión y Resultados

Con estas modificaciones, el flujo de onboarding garantiza que el recolector recibe un documento de consentimiento personalizado con su información real y de manera segura. El sistema de sincronización queda protegido ante ciclos de error indefinidos gracias a la política de reintentos con límite de 3 intentos.

#### Resultados Obtenidos

| Indicador | Valor |
|---|---|
| Período de implementación | 30 Mar – 8 Abr 2026 |
| Duración total | 10 días |
| Versiones generadas | v1.1.0 y v1.2.0 |
| Componentes impactados | 1 (Mobile Android) |
| Mecanismo de cifrado | RSA-OAEP + AES-256-GCM |
| Fallback implementado | Sí (endpoint GET sin cifrar) |
