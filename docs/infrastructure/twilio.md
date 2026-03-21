# Integración Twilio & Meta (MVP / Pre-Producción)

Estos proveedores externos proveen la pasarela de telecomunicaciones fundamental para el manejo conversacional corporativo y la seguridad telefónica.

## Cuentas

- **Cuenta de Twilio:** `[Pendiente de definir]`
- **Cuenta de Meta Empresarial:** `[Pendiente de definir]`

## Integraciones y Configuraciones Cloud

### OTP & Telefonía (Twilio)

- **Twilio Verify API:**
    - Utilizado y provisto para los métodos de verificación en la capa de inicio de sesión o creación (SMS OTP).
    - Orquestado técnica y lógicamente de exclusión por medio de llamadas salientes directas desde `pachamama-api-admin-java`.

### WhatsApp Business (Meta)

- Se encuentra planificado (o en transición) apoyarse en los canales aprobados por **Business de Meta** (probablemente con webhook intermediario en un API) para notificar desde un canal oficial certificado a los recolectores de campo que operan mediante canales paralelos corporativos.