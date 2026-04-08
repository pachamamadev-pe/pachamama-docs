# Pachamama Web Landing Page (MVP / Pre-Producción)

Esta es la web de landing (promocional o informativa) alojada en la capa gratuita de Vercel. Esta configuración inicial corresponde al entorno de pre-producción vinculado a la arquitectura MVP.

## Enlaces y Cuentas

- **URL Pública:** [https://pachamama-web-landing-v1.vercel.app/](https://pachamama-web-landing-v1.vercel.app/)
- **Cuenta (Correo Administrador):** `jecrido@gmail.com`
- **Ajustes de Vercel (URL del Proyecto):** [Ver en Vercel](https://vercel.com/jecridosantos-projects/pachamama-web-landing-v1/settings)

## Sistema de Control de Versiones (Repositorios)

- **Repo Original (Organización):** [https://github.com/pachamamadev-pe/pachamama-web-landing](https://github.com/pachamamadev-pe/pachamama-web-landing)
- **Repo Integrado a Vercel:** [https://github.com/jecridosantos/pachamama-web-landing-v1](https://github.com/jecridosantos/pachamama-web-landing-v1) 
*(Nota: Debido a que la cuenta de Vercel es gratuita, no fue posible conectarla directamente a un repositorio bajo la organización de Github, por lo cual se integró a este fork en una cuenta de usuario normal).*

## Configuración de Despliegue (Framework Settings Vercel)

- **Framework Preset:** Vite
- **Node.js Version:** `24.x`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install`
- **Development Command:** `vite`

## Dominio Personalizado

> ⚠️ Configuración actual bajo cuenta personal `jecrido@gmail.com`. **Pendiente de migrar a Azure Static Web Apps** (ver [Fase 3 del Roadmap](../../ROADMAP-MIGRATION-PRD.md)).

- **Subdominio:** `landing.pachamama.eco`
- **URL Pública:** [https://landing.pachamama.eco](https://landing.pachamama.eco)
- **Tipo de registro DNS:** CNAME
- **Valor DNS (Vercel):** `69cba288a6086eb9.vercel-dns-017.com`

## Infraestructura de Costeo de Build

- **Build Machine:** Standard (4 vCPUs, 8 GB RAM)
- **On-Demand Concurrent Builds:** Disable on-demand concurrent builds
