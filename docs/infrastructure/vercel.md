# Plataforma Vercel (MVP / Pre-Producción)

Los servicios de Frontend de la plataforma están alojados y desplegados utilizando la capa gratuita de **Vercel**. 

## Cuentas

A continuación el registro de correos vinculados para administrar los paneles de Vercel en la fase de MVP:

| Cuenta (Correo) | Proyecto(s) a cargo |
|---|---|
| jecrido@gmail.com | Landing Page (pachamama-web-landing-v1) |
| ricardoalvaradoaponte@gmail.com | Admin Web (web-admin-pachamama) |

## Integraciones y Configuraciones Cloud

### Mapeo de Aplicaciones (Apps)

| Repositorio de Código | Proyecto en Vercel | URL Pública |
|---|---|---|
| pachamama-web-landing-v1 (GitHub Fork) | pachamama-web-landing-v1 | [Abrir](https://pachamama-web-landing-v1.vercel.app/) <br> [landing.pachamama.eco](https://landing.pachamama.eco) |
| pachamama-web-admin (GitHub Org) | web-admin-pachamama | [Abrir](https://web-admin-pachamama.vercel.app/) <br> [app.pachamama.eco](https://app.pachamama.eco) |

### Dominios Personalizados

> ⚠️ Los dominios personalizados configurados en Vercel están bajo cuentas personales. **Deben migrarse a Azure Static Web Apps** en la Fase 3 del Roadmap. Al migrar, los registros DNS deben actualizarse en SiteGround para apuntar a Azure en lugar de Vercel.

| Proyecto Vercel | Cuenta | Subdominio | Tipo Registro | Valor DNS |
|---|---|---|---|---|
| pachamama-web-landing-v1 | `jecrido@gmail.com` | `landing.pachamama.eco` | CNAME | `69cba288a6086eb9.vercel-dns-017.com` |
| web-admin-pachamama | `ricardoalvaradoaponte@gmail.com` | `app.pachamama.eco` | CNAME | `28b117c987ffc012.vercel-dns-017.com` |

### Gestión del Dominio Principal (SiteGround)

El dominio `pachamama.eco` está administrado desde **SiteGround**. Desde allí se gestionan los registros DNS de todos los subdominios. Los subdominios `landing.pachamama.eco` y `app.pachamama.eco` fueron creados en SiteGround y sus registros DNS configurados para apuntar a Vercel.

**Registros DNS actuales en SiteGround:**

| Tipo | Nombre | Valor |
|---|---|---|
| `TXT` | `_vercel.pachamama.eco.` | `vc-domain-verify=app.pachamama.eco,84a79342862139b3fa83` |
| `CNAME` | `app.pachamama.eco.` | `28b117c987ffc012.vercel-dns-017.com` |
| `CNAME` | `landing.pachamama.eco.` | `69cba288a6086eb9.vercel-dns-017.com` |

> 📝 El registro TXT `_vercel` es requerido por Vercel para la verificación de propiedad del dominio. Al migrar a Azure Static Web Apps, este registro deberá eliminarse o reemplazarse por el equivalente de verificación de Azure, y los CNAME deberán actualizarse a los endpoints de Azure.

### Configuración Vercel y GitHub

Vercel está directamente **integrado con los repositorios de GitHub** a través de su App oficial.
A nivel infraestructura o plataforma, estas son las configuraciones de los proyectos de Vercel:

- **Environment:** Node.js (v24.x)
- **Framework Preset:** Vite
- **Build Machine:** Standard (4 vCPUs, 8 GB RAM)
- **On-Demand concurrent builds:** Disabled

**Flujo de Despliegue:**
No se utilizan flujos de GitHub Actions propios; la integración es nativa de Vercel. Cada **push** o **merge** aceptado sobre la rama base configurada de los repositorios enlazados dispara la recostrucción utilizando **npm run build** y exposición del **dist** a través del CDN nativo.
