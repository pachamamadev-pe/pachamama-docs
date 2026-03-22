# Comunicaciones y Meta (Twilio)

Pachamama utiliza la plataforma de **Twilio** acoplada con el ecosistema de **Meta** para proveer servicios de mensajería y verificación de identidad a doble factor (MFA/OTP), garantizando el acceso seguro al sistema.

## Estrategia de Comunicación

Para validar la identidad del usuario durante el login o transacciones críticas, el sistema se apoya en el envío de códigos de un solo uso (OTP).
- **Canal Principal (Priorizado):** WhatsApp.
- **Canal Secundario (Despriorizado/Respaldo):** SMS Tradicional.

---

## Configuración de la Cuenta base (Twilio)

- **Cuenta Administradora:** pachamamadev@gmail.com
- **Account SID:** AC******************************
- **Modelo de Facturación:** Pay-as-you-go (Pago por consumo / mensaje exitoso).

---

## Integración con Meta (WhatsApp Business)

Para lograr el envío oficial y evitar baneos de SPAM, la cuenta de Twilio está vinculada directamente al Meta Business Manager compartiendo el mismo correo administrador.

### Datos del Sender (Remitente Oficial)
- **WhatsApp Number (Sender):** +1555******
- **Nombre Comercial (Display Name):** Pachamama.bosques
- **WhatsApp Business Account ID (WABA):** 1403********9400
- **Meta Business Manager ID:** 1986********1722

---

## Servicios Activos (Twilio Verify)

En lugar de construir la lógica de expiración, reintentos y generación aleatoria del propio código, se utiliza el producto gestionado **Twilio Verify API**:

- **Nombre del Verify Service:** Pachamama-OTP-WhatsApp
- **Verify Service SID:** VA******************************
- **Canal Habilitado:** Exclusivamente configurado para despachar vía la plantilla oficial de OTP de WhatsApp.
