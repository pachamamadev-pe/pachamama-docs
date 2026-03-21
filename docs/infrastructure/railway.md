# Plataforma Railway (MVP / Pre-Producción)

**Railway** se utiliza para alojar la base de datos relacional transaccional, con soporte robusto para componentes geoespaciales críticos para la plataforma.

## Cuentas

- **Cuenta Principal / Equipo:** `[Pendiente de definir]`
- **Uso:** Alojamiento de clúster de base de datos PostgreSQL en cloud de fácil acceso.

## Integraciones y Configuraciones Cloud

### Base de Datos Relacional

- **Motor de Base de Datos:** PostgreSQL
- **Extensión Espacial:** PostGIS (esencial para el trackeo de mapas, polígonos satelitales y gestión geográfica de lotes).
- **Consumidores Principales Integrados:** 
    - `pachamama-api-admin-java` (Persistencia general y operativa)
    - `pachamama-api-sync-java` (Persistencia asíncrona para inserciones batch de recolectores).