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
| pachamama-web-admin (GitHub Org) | web-admin-pachamama | [Abrir](https://web-admin-pachamama.vercel.app/) |

### Dominios Personalizados

> ⚠️ Los dominios personalizados configurados en Vercel corresponden a la cuenta personal `jecrido@gmail.com`. **Deben migrarse a Azure Static Web Apps** en la Fase 3 del Roadmap.

| Proyecto Vercel | Subdominio | Tipo Registro | Valor DNS |
|---|---|---|---|
| pachamama-web-landing-v1 | `landing.pachamama.eco` | CNAME | `69cba288a6086eb9.vercel-dns-017.com` |

### Configuración Vercel y GitHub

Vercel está directamente **integrado con los repositorios de GitHub** a través de su App oficial.
A nivel infraestructura o plataforma, estas son las configuraciones de los proyectos de Vercel:

- **Environment:** Node.js (v24.x)
- **Framework Preset:** Vite
- **Build Machine:** Standard (4 vCPUs, 8 GB RAM)
- **On-Demand concurrent builds:** Disabled

**Flujo de Despliegue:**
No se utilizan flujos de GitHub Actions propios; la integración es nativa de Vercel. Cada **push** o **merge** aceptado sobre la rama base configurada de los repositorios enlazados dispara la recostrucción utilizando **npm run build** y exposición del **dist** a través del CDN nativo.
