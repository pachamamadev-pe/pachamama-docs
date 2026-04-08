# Changelog — Pachamama API Admin (Java)

**Cambio Relacionado:** Consentimiento Informado Cifrado — Onboarding de Recolectores  
**Fecha:** Abril 2026

---

## Resumen Ejecutivo

Se implementó un nuevo endpoint cifrado para obtener el documento de consentimiento informado
con los datos del recolector y la empresa reemplazados dinámicamente antes de ser entregado
al dispositivo móvil.

El documento resultante incluye el nombre del recolector, DNI, razón social y RUC de la empresa
contratante, y datos estáticos de la plataforma (región Azure, contacto ARCO, RUC de Reori),
eliminando la necesidad de que el frontend haga esos reemplazos en el cliente.

---

## Nuevo Endpoint

### `POST /api/v1/collectors/onboarding/legal-documents/encrypted`

Recibe el payload cifrado (mismo esquema que `POST /onboarding/encrypted`), lo descifra con la
clave privada RSA del servidor, resuelve el contexto del recolector y la empresa a través del
token de invitación, y devuelve el documento legal con todos los parámetros `[[...]]`
reemplazados.

- **Cuando `type = "consent"`:** procesamiento completo — se resuelve la empresa desde `invitationToken` (QR o código corto vía Redis) y se reemplazan los 9 parámetros dinámicos.
- **Cuando `type = "privacy"` o `"terms"`:** se devuelve el documento tal cual, sin necesidad de pasar token de invitación.
- **Autenticación:** HTTP Basic (igual que el resto de endpoints de onboarding).

#### Request — sobre cifrado (body)

```json
{
  "keyId": "onboarding-key-v1",
  "encryptedKeyBase64": "<RSA-OAEP(AES key)>",
  "ivBase64": "<IV 12 bytes en Base64>",
  "encryptedPayloadBase64": "<AES-256-GCM(payload JSON) en Base64>"
}
```

#### Payload JSON descifrado

| Campo | Tipo | Requerido | Descripción |
|---|---|:---:|---|
| `type` | `String` | ✅ | `consent`, `privacy` o `terms` |
| `invitationToken` | `String` | ⚠️ Solo `consent` | JWT del QR o código corto |
| `invitationType` | `Enum` | ⚠️ Solo `consent` | `QR` o `SHORT_CODE` |
| `versionApp` | `String` | ⚠️ Solo `consent` | Versión de la app móvil |
| `collectorName` | `String` | ⚠️ Solo `consent` | Nombre completo del recolector |
| `dni` | `String` | ⚠️ Solo `consent` | DNI del recolector (8 dígitos) |

**Ejemplo `type = "consent"`:**
```json
{
  "type": "consent",
  "invitationToken": "eyJhbGciOiJIUzI1NiJ9...",
  "invitationType": "QR",
  "versionApp": "1.2.0",
  "collectorName": "JECRI REY DO SANTOS OCMIN",
  "dni": "48268692"
}
```

**Ejemplo `type = "privacy"` o `"terms"`:**
```json
{ "type": "privacy" }
```

#### Response `200 OK`

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "type": "consent",
  "version": "2026-03-01",
  "content": "# Consentimiento Informado\n\n**Versión:** 1.2.0\n\n**Recolector:** JECRI REY DO SANTOS OCMIN\n...",
  "publishedAt": "2026-03-01T00:00:00Z"
}
```

> El campo `version` debe guardarse en el cliente y enviarse como `consentVersion` al completar el onboarding en `POST /onboarding/encrypted`.

#### Parámetros reemplazados en el documento (solo `type = "consent"`)

| Parámetro | Fuente |
|---|---|
| `[[VERSION]]` | `request.versionApp` |
| `[[NOMBRE_RECOLECTOR]]` | `request.collectorName` |
| `[[DNI_RECOLECTOR]]` | `request.dni` |
| `[[RAZON_SOCIAL_CLIENTE]]` | `company.businessName` (resuelto desde invitationToken) |
| `[[RUC_CLIENTE]]` | `company.ruc` |
| `[[DIRECCION_CLIENTE]]` | `company.taxAddress` |
| `[[REGION_AZURE]]` | Propiedad `app.legal.azure-region` |
| `[[CONTACTO_ARCO]]` | Propiedad `app.legal.contacto-arco` |
| `[[RUC_REORI]]` | Propiedad `app.legal.ruc-reori` |

#### Códigos de Error

| HTTP | Situación |
|---|---|
| `400` | Payload cifrado mal formado, `keyId` incorrecto o campos faltantes para `consent` |
| `401` | Credenciales Basic incorrectas |
| `404` | No existe documento publicado para el `type` indicado |
| `422` | `invitationToken` inválido, expirado o `invitationType` incorrecto |

---

## Cambios Técnicos Aplicados

### Nuevas Clases y Archivos

| Clase | Módulo | Descripción |
|---|---|---|
| `LegalDocumentRequestDto` | `collectors` | Payload descifrado del nuevo endpoint |
| `LegalDocumentServiceImpl#getLatestByTypeWithContext` | `collectors` | Resolución de empresa, parseo del JWT de invitación y reemplazo de parámetros |
| `OnboardingCryptoService#decryptLegalDocument` | `collectors` | Descifra el sobre RSA+AES-GCM y deserializa a `LegalDocumentRequestDto` |

### Cambios en Clases Existentes

| Clase | Cambio |
|---|---|
| `LegalDocumentService` | Nuevo método de interfaz `getLatestByTypeWithContext(LegalDocumentRequestDto)` |
| `LegalDocumentServiceImpl` | Refactor del constructor: eliminado `@RequiredArgsConstructor`, se inyecta `pachamama.jwt.invitation.secret` para construir la `SecretKey` del JWT |
| `OnboardingCryptoService` | Nuevo método `decryptLegalDocument()` reutilizando lógica RSA-OAEP + AES-256-GCM |
| `CollectorOnboardingController` | Nuevo endpoint `POST /legal-documents/encrypted` con documentación Swagger completa |

### Nuevas Propiedades de Configuración

Agregar en `application.yaml`:

```yaml
app:
  legal:
    azure-region: "US East (Virginia, USA)"
    contacto-arco: "999 999 999"
    ruc-reori: "20603056338"
```

### Comportamiento del Caché Redis

Al resolver el token de tipo `SHORT_CODE`, se usa `redisTemplate.opsForValue().get(key)`
**sin delete y sin modificar el TTL**. El token permanece disponible para el onboarding
completo que ocurre en el siguiente paso del flujo.

---

## Endpoint Existente (sin cambios)

```
GET /api/v1/collectors/onboarding/legal-documents/{type}
```

Devuelve el documento sin procesar parámetros. Sigue siendo válido para casos sin
necesidad de personalización (previsualización antes de ingresar datos del recolector).
