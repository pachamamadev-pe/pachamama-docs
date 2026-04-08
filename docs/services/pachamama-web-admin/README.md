# Pachamama Web Admin (MVP / Pre-Producción)

Esta es la web de administración (panel de control) alojada en la capa gratuita de Vercel. Esta configuración inicial corresponde al entorno de pre-producción vinculado a la arquitectura MVP.

## Enlaces y Cuentas

- **URL Pública:** [https://web-admin-pachamama.vercel.app/](https://web-admin-pachamama.vercel.app/)
- **Cuenta (Correo Administrador):** `ricardoalvaradoaponte@gmail.com`
- **Ajustes de Vercel (URL del Proyecto):** [Ver en Vercel](https://vercel.com/ricardo-alvarados-projects/web-admin-pachamama/settings)

## Sistema de Control de Versiones (Repositorios)

- **Repo Integrado a Vercel:** [https://github.com/pachamamadev-pe/pachamama-web-admin](https://github.com/pachamamadev-pe/pachamama-web-admin) 
*(Nota: En este proyecto sí fue posible enlazar directamente al repositorio original bajo la organización de Github).*

## Configuración de Despliegue (Framework Settings Vercel)

- **Framework Preset:** Vite
- **Node.js Version:** `24.x`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install`
- **Development Command:** `vite`

## Dominio Personalizado

> ⚠️ Configuración actual bajo cuenta personal `ricardoalvaradoaponte@gmail.com`. **Pendiente de migrar a Azure Static Web Apps** (ver [Fase 3 del Roadmap](../../ROADMAP-MIGRATION-PRD.md)). El registro DNS está gestionado desde **SiteGround** (dominio `pachamama.eco`).

- **Subdominio:** `app.pachamama.eco`
- **URL Pública:** [https://app.pachamama.eco](https://app.pachamama.eco)
- **Tipo de registro DNS:** CNAME
- **Valor DNS (Vercel):** `28b117c987ffc012.vercel-dns-017.com`

## Infraestructura de Costeo de Build

- **Build Machine:** Standard (4 vCPUs, 8 GB RAM)
- **On-Demand Concurrent Builds:** Disable on-demand concurrent builds
