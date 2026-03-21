# Roles y Permisos del Sistema (MVP)

> **Nota para MVP:** En esta primera versión (MVP), los roles y permisos se configuran de manera directa mediante parametrización en la base de datos, puntualmente a través de la tabla `core.roles`.

---

## Catálogo de permisos con descripción

### Global

* `*:*` — Acceso total a todas las funciones del sistema.


### Company

* `company:*` — Gestión completa de empresa
* `company:read` — Ver/listar empresas.
* `company:create` — Crear empresa.
* `company:update` — Editar, activar y desactivar empresa.
* `company:delete` — Eliminar empresa.
* `company:manage_documents` — Gestionar documentos de empresa.
* `company:manage_admins` — Gestionar administradores de empresa.

### Community

* `community:*` — Gestión completa de comunidades (crear, editar, listar, eliminar, etc.).
* `community:read` — Ver lista de comunidades / ver detalle de comunidades.
* `community:create` — Crear comunidad.
* `community:update` — Editar comunidad.
* `community:delete` — Eliminar comunidad.

### Product

* `product:*` — Gestión completa de productos
* `product:read` — Ver productos y detalle por producto.
* `product:create` — Crear producto.
* `product:update` — Editar datos de producto. Protocolos del producto.
* `product:delete` — Eliminar producto.


### User

* `user:*` — Gestión completa de usuarios
* `user:read` — Ver/listar usuarios.
* `user:create` — Crear usuario.
* `user:update` —  Editar usuario y cambiar rol.
* `user:delete` — Desactivar usuario.

### Profile

* `profile:*` — Gestión de perfil (datos del usuario, ajustes, cambio de contraseña, etc.).
  *(En su mayoría es “mi perfil / configuración personal”.)*

### Form

* `form:*` — Gestión completa de formularios dinámicos
* `form:read` — Listar formularios dinámicos. Ver historial formulario dinámico.
* `form:create` — Crear formulario dinámico.
* `form:update` — Editar, copiar formulario dinámico.
* `form:delete` — Archivar formulario dinámico.
* `form:publish` — Publicar/despublicar formulario dinámico.

### Project (CRUD / acceso base)

* `project:read` — Ver/listar proyectos y entrar al detalle.
* `project:create` — Crear proyectos.
* `project:update` — Editar/actualizar proyectos.
* `project:upload_map` — Cargar/actualizar mapa del área del proyecto (ZIP, SHP, KML, KMZ, GeoJSON).
* `project:next_stage` — Activar la etapa de: inventario del proyecto/ generación/edición de PMF dentro de la plataforma / recolección.
* `project:generation_pmf` — Generar PMF en base al proyecto.

### Documentos del proyecto

* `document:*` — Gestionar documentos del proyecto
* `document:read` — Ver documentos del proyecto
* `document:upload` — Subir documentos del proyecto
* `document:download` — Descargar documento del proyecto
* `document:review` — Revisar documento del proyecto: aprobar/observar/rechazar

### Registro de actividades del proyecto

* `activity_inventory:*` — Gestión completa de actividades de inventario
* `activity_inventory:read` — Ver/listar actividades de inventario.
* `activity_inventory:review` — Aprobar actividades de inventario.
* `activity_collection:*` — Gestión completa de actividades de recolección
* `activity_collection:read` — Ver/listar actividades de recolección.
* `activity_collection:review` — Aprobar actividades de recolección.

### Solicitudes de recolección del proyecto
* `collection_request:*` — Gestión completa de solicitudes de recolección
* `collection_request:read` — Ver/listar solicitudes de recolección
* `collection_request:create` — Crear solicitud de recolección
* `collection_request:update` — Editar solicitud de recolección
* `collection_request:review` — Aprobar/observar/rechazar solicitud de recolección

### Lotes de acopio del proyecto

* `collection_batch:*` — Gestión completa de lotes de acopio
* `collection_batch:read` — Ver lotes de acopio y detalle de documentos generados.
* `collection_batch:create` — Crear lote de acopio.
* `collection_batch:process` — Completar y guardar documentos de acopio.

### Configuración del proyecto (columnas calculadas y agregaciones)
* `activity_formula:*` — Gestión completa de fórmulas de actividad
* `activity_formula:read` — Ver fórmulas de actividad.
* `activity_formula:create` — Crear fórmula de actividad.
* `activity_formula:update` — Editar fórmula de actividad.
* `activity_formula:delete` — Archivar fórmula de actividad.
* `project_aggregation:*` — Gestión completa de agregaciones de proyecto
* `project_aggregation:read` — Ver agregaciones de proyecto.
* `project_aggregation:create` — Crear agregación de proyecto.
* `project_aggregation:update` — Editar agregación de proyecto.
* `project_aggregation:delete` — Archivar agregación de proyecto.


### Collector

* `collector:*` — Gestión completa de recolectores
* `collector:read` — Ver Recolectores asignados al proyecto, ver historial de cambios.
* `collector:update` — Cambiar estado de recolectores.

### Brigade

* `brigade:*` — Gestión completa de brigadas
* `brigade:read` — Ver brigadas asignadas al proyecto. Ver recolectores asignados a la brigada.
* `brigade:create` — Crear brigada. Ver solicitudes aprobadas.
* `brigade:update` — Editar datos de la brigada, cambiar de estado y añadir recolectores.

### Tipos de documento de la empresa
* `document_type:*` — Gestión completa de tipos de documento de la empresa.
* `document_type:read` — Ver/listar tipos de documento de la empresa. Ver detalle de tipo de documento.
* `document_type:create` — Crear tipo de documento de la empresa, puede ser nuevo o customizar un global.
* `document_type:update` — Editar tipo de documento de la empresa.
* `document_type:delete` — Archivar tipo de documento de la empresa.


### Transformación primaria
* `transformation_primary:*` — Gestión completa de lotes de transformación primaria.
* `transformation_primary:read` — Ver lotes de transformación primaria.
* `transformation_primary:create` — Crear lote de transformación primaria.
* `transformation_primary:process` — Completar y guardar documentos por cada etapa de transformación primaria.
* `transformation_primary:generate_qr` — Generar QR para lote de transformación primaria.
* `transformation_primary:view_location` — Ver ubicación de lote de transformación primaria.
* `transformation_primary:storage` — Completar y guardar documento en la etapa de almacenamiento.

### Transformación secundaria
* `transformation_secondary:*` — Gestión completa de lotes de transformación secundaria.
* `transformation_secondary:read` — Ver lotes de transformación secundaria.
* `transformation_secondary:create` — Crear lote de transformación secundaria.
* `transformation_secondary:process` — Completar y guardar documentos por cada etapa de transformación secundaria.
* `transformation_secondary:generate_qr` — Generar QR para lote de transformación secundaria.
* `transformation_secondary:view_location` — Ver ubicación de lote de transformación secundaria.


### Dashboard empresarial

* `dashboard:*` — Todos los permisos para dashboard.
* `dashboard:view` — Ver dahboard empresarial.

---

## Resumen rápido por rol (para ubicarte)

### ADMIN_PACHAMAMA

- Todo (`*:*`).

### ADMIN_EMPRESA

- Admin total de la operación de empresa: `company:*`, `project:*`, `payment:*`, `collector:*`, `brigade:*`, `activity:*`.
- En la práctica: ve y hace casi todo, pero **solo dentro de su empresa/tenant**.

### GESTOR_RELACIONAMIENTO_COMUNITARIO

- Dominio “arranque” del flujo: comunidades, formularios, usuarios, perfil.
- En proyectos: crea/edita, mapas, inventario, PMF (generación/aprobación/docs), documentos, activa recolección, crea órdenes y genera órdenes de pago.

### GESTOR_TRANSFORMACION_PRIMARIA

- Entra a proyectos (read) y ejecuta la etapa de transformación primaria:
  - recepción y procesamiento de recolección
  - transformación primaria
  - emisión de lote de producción
  - usa formularios dinámicos y perfil.

### GESTOR_ALMACENAMIENTO_TEMPORAL

- Ve proyectos y documentos.
- Aprueba recepción de lotes, registra entrega de lotes.
- Puede registrar/subir documentos del proyecto (ojo: esto es fuerte; puede ser intencional).

### GESTOR_TRANSFORMACION_SECUNDARIA

- Ve proyectos y documentos.
- Aprueba recepción de lote terminado.

### RECOLECTOR_ADMINISTRADOR

- Perfil + lectura de proyectos.
- Aprueba solicitudes de recolección (`collection:approve_requests`).
- Maneja brigadas (`brigade:*`).

---

## Observaciones rápidas (para afinar después sin fricción)

Perfecto Ray. Aquí va:

1. **Matriz Roles × Permisos (con ✅)**
2. **Primer borrador de `PERMISSIONS.ts`** (listo para copiar/pegar y seguir alimentando)

---

## Matriz Roles × Permisos

**Roles (columnas):**

- **AP** = ADMIN_PACHAMAMA
- **AE** = ADMIN_EMPRESA
- **GRC** = GESTOR_RELACIONAMIENTO_COMUNITARIO
- **GTP** = GESTOR_TRANSFORMACION_PRIMARIA
- **GAT** = GESTOR_ALMACENAMIENTO_TEMPORAL
- **GTS** = GESTOR_TRANSFORMACION_SECUNDARIA
- **RA** = RECOLECTOR_ADMINISTRADOR

| Permiso                                  | Descripción breve                                    | AP  | AE  | GRC | GTP | GAT | GTS | RA  |
| ---------------------------------------- | ---------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `company:*`                              | Gestión completa de empresa                          | ✅  |     |     |     |     |     |     |
| `company:create`                         | Crear empresa                                        | ✅  |     |     |     |     |     |     |
| `company:read`                           | Ver/listar empresas                                  | ✅  |     |     |     |     |     |     |
| `company:update`                         | Editar, activar y desactivar empresa                 | ✅  |     |     |     |     |     |     |
| `company:delete`                         | Eliminar empresa                                     | ✅  |     |     |     |     |     |     |
| `company:manage_documents`               | Gestionar documentos de empresa                      | ✅  |     |     |     |     |     |     |
| `company:manage_admins`                  | Gestionar administradores de empresa                 | ✅  |     |     |     |     |     |     |
| `project:*`                              | Gestión completa de proyectos (todas acciones)       | ✅  | ✅  |     |     |     |     |     |
| `collector:*`                            | Gestión completa de recolectores                     |     | ✅  | ✅  |     |     |     | ✅  |
| `collector:read`                         | Ver recolectores asignados al proyecto               |     | ✅  | ✅  |     |     |     | ✅  |
| `collector:update`                       | Cambiar estado de recolectores                       |     | ✅  | ✅  |     |     |     | ✅  |
| `brigade:*`                              | Gestión completa de brigadas                         |     | ✅  | ✅  |     |     |     | ✅  |
| `brigade:read`                           | Ver brigadas, recolectores asignados                 |     | ✅  | ✅  |     |     |     | ✅  |
| `brigade:create`                         | Crear brigada. Ver solicitudes aprobadas             |     | ✅  | ✅  |     |     |     | ✅  |
| `brigade:update`                         | Edita datos de brigada, estado y añadir recolector   |     | ✅  | ✅  |     |     |     | ✅  |
| `community:*`                            | Gestión completa de comunidades                      |     | ✅  | ✅  |     |     |     |     |
| `community:read`                         | Ver comunidades. Ver detalles                        |     | ✅  | ✅  |     |     |     |     |
| `community:create`                       | Crear comunidad                                      |     | ✅  | ✅  |     |     |     |     |
| `community:update`                       | Editar datos de comunidad                            |     | ✅  | ✅  |     |     |     |     |
| `community:delete`                       | Eliminar comunidad                                   |     | ✅  | ✅  |     |     |     |     |
| `product:*`                              | Gestión completa de productos                        |     | ✅  | ✅  |     |     |     |     |
| `product:read`                           | Ver productos y detalle de producto                  |     | ✅  | ✅  |     |     |     |     |
| `product:create`                         | Crear productos                                      |     | ✅  | ✅  |     |     |     |     |
| `product:update`                         | Editar datos de producto y sus protocolos            |     | ✅  | ✅  |     |     |     |     |
| `product:delete`                         | Eliminar producto                                    |     | ✅  | ✅  |     |     |     |     |
| `form:*`                                 | Gestión completa de formularios dinámicos            |     | ✅  | ✅  | ✅  |     | ✅  |     |
| `form:read`                              | Listar formularios dinámicos. Ver historial          |     | ✅  | ✅  | ✅  |     | ✅  |     |
| `form:create`                            | Crear formularios dinámicos.                         |     | ✅  | ✅  | ✅  |     | ✅  |     |
| `form:update`                            | Editar, copiar formulario dinámico                   |     | ✅  | ✅  | ✅  |     | ✅  |     |
| `form:delete`                            | Archivar formulario dinámico                         |     | ✅  | ✅  | ✅  |     | ✅  |     |
| `form:publish`                           | Publicar/despublicar formulario dinámico             |     | ✅  | ✅  | ✅  |     | ✅  |     |
| `user:*`                                 | Gestión completa de usuarios                         |     | ✅  |     |     |     |     |     |
| `user:read`                              | Ver/listar usuarios                                  |     | ✅  |     |     |     |     |     |
| `user:create`                            | Crear usuarios                                       |     | ✅  |     |     |     |     |     |
| `user:update`                            | Editar usuario y cambiar rol                         |     | ✅  |     |     |     |     |     |
| `user:delete`                            | Desactivar usuario                                   |     | ✅  |     |     |     |     |     |
| `profile:*`                              | Perfil/ajustes del usuario                           | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |
| `project:read`                           | Ver/listar proyectos y detalle                       |     | ✅  | ✅  | ✅  | ✅  | ✅  | ✅  |
| `project:create`                         | Crear proyectos                                      |     | ✅  | ✅  |     |     |     |     |
| `project:update`                         | Editar proyectos                                     |     | ✅  | ✅  |     |     |     |     |
| `project:delete`                         | Eliminar proyecto                                    |     | ✅  | ✅  |     |     |     |     |
| `project:upload_map`                     | Subir mapa del área del proyecto                     |     | ✅  | ✅  |     |     |     |     |
| `project:next_stage`                     | Activar la siguiente etapa del proyecto              |     | ✅  | ✅  |     |     |     |     |
| `project:generation_pmf`                 | Generar PMF en base al proyecto                      |     | ✅  | ✅  |     |     |     |     |
| `document:*`                             | Gestionar documentos del proyecto                    |     | ✅  | ✅  |     |     |     |     |
| `document:read`                          | Ver documentos del proyecto                          |     | ✅  | ✅  |     |     |     |     |
| `document:upload`                        | Subir documentos del proyecto                        |     | ✅  | ✅  |     |     |     |     |
| `document:download`                      | Descargar documento del proyecto                     |     | ✅  | ✅  |     |     |     |     |
| `document:review`                        | Revisar documento del proy: aprob/observ/rechaz      |     | ✅  |     |     |     |     |     |
| `activity_inventory:*`                   | Gestión completa de actividades de inventario        |     | ✅  | ✅  |     |     |     | ✅  |
| `activity_inventory:read`                | Ver/listar actividades de inventario                 |     | ✅  | ✅  |     |     |     | ✅  |
| `activity_inventory:review`              | Aprobar actividades de inventario                    |     | ✅  | ✅  |     |     |     | ✅  |
| `activity_collection:*`                  | Gestión completa de actividades de recolección       |     | ✅  | ✅  |     |     |     | ✅  |
| `activity_collection:read`               | Ver/listar actividades de recolección                |     | ✅  | ✅  |     |     |     | ✅  |
| `activity_collection:review`             | Aprobar actividades de recolección                   |     | ✅  | ✅  |     |     |     | ✅  |
| `collection_request:*`                   | Gestión completa de solicitudes de recolección       |     | ✅  | ✅  |     |     |     | ✅  |
| `collection_request:read`                | Ver/listar solicitudes de recolección                |     | ✅  | ✅  |     |     |     | ✅  |
| `collection_request:create`              | Crear solicitud de recolección                       |     | ✅  | ✅  |     |     |     | ✅  |
| `collection_request:update`              | Editar solicitud de recolección                      |     | ✅  | ✅  |     |     |     | ✅  |
| `collection_request:review`              | Aprobar/observar/rechazar solicitud de recolección   |     | ✅  | ✅  |     |     |     | ✅  |
| `collection_batch:*`                     | Gestión completa de lotes de acopio                  |     | ✅  | ✅  |     |     |     |     |
| `collection_batch:read`                  | Ver lotes de acopio y detalle de documentos gen.     |     | ✅  | ✅  |     |     |     |     |
| `collection_batch:create`                | Crear lote de acopio                                 |     | ✅  | ✅  |     |     |     |     |
| `collection_batch:process`               | Completar y guardar documentos de acopio             |     | ✅  | ✅  |     |     |     |     |
| `activity_formula:*`                     | Gestión completa de fórmulas de actividad            |     | ✅  | ✅  |     |     |     |     |
| `activity_formula:read`                  | Ver fórmulas de actividad                            |     | ✅  | ✅  |     |     |     |     |
| `activity_formula:create`                | Crear fórmula de actividad                           |     | ✅  | ✅  |     |     |     |     |
| `activity_formula:update`                | Editar fórmula de actividad                          |     | ✅  | ✅  |     |     |     |     |
| `activity_formula:delete`                | Archivar fórmula de actividad                        |     | ✅  | ✅  |     |     |     |     |
| `project_aggregation:*`                  | Gestión completa de agregaciones de proyecto         |     | ✅  | ✅  |     |     |     |     |
| `project_aggregation:read`               | Ver agregaciones de proyecto                         |     | ✅  | ✅  |     |     |     |     |
| `project_aggregation:create`             | Crear agregación de proyecto                         |     | ✅  | ✅  |     |     |     |     |
| `project_aggregation:update`             | Editar agregación de proyecto                        |     | ✅  | ✅  |     |     |     |     |
| `project_aggregation:delete`             | Archivar agregación de proyecto                      |     | ✅  | ✅  |     |     |     |     |
| `document_type:*`                        | Gestión de tipos de documento de la empresa          |     | ✅  |     |     |     |     |     |
| `document_type:read`                     | Ver/listar tipos de documento de la empresa          |     | ✅  |     |     |     |     |     |
| `document_type:create`                   | Crear tipo de documento nuevo o customizar global    |     | ✅  |     |     |     |     |     |
| `document_type:update`                   | Editar tipo de documento de la empresa               |     | ✅  |     |     |     |     |     |
| `document_type:delete`                   | Archivar tipo de documento de la empresa             |     | ✅  |     |     |     |     |     |
| `transformation_primary:*`               | Gestión completa de lotes de transformación primaria |     | ✅  |     | ✅  |     |     |     |
| `transformation_primary:read`            | Ver lotes de transformación primaria                 |     | ✅  |     | ✅  | ✅  |     |     |
| `transformation_primary:create`          | Crear lote de transformación primaria                |     | ✅  |     | ✅  |     |     |     |
| `transformation_primary:process`         | Completar y guardar documentos por etapas de TF      |     | ✅  |     | ✅  |     |     |     |
| `transformation_primary:generate_qr`     | Generar QR para lote de transformación primaria      |     | ✅  |     | ✅  |     |     |     |
| `transformation_primary:view_location`   | Ver ubicación de lote de transformación primaria     |     | ✅  |     | ✅  |     |     |     |
| `transformation_primary:storage`         | Completar y guardar documento en E. almacenamiento   |     | ✅  |     | ✅  | ✅  |     |     |
| `transformation_secondary:*`             | Gestión completa de lotes de transform secundaria    |     | ✅  |     |     |     | ✅  |     |
| `transformation_secondary:read`          | Ver lotes de transformación secundaria               |     | ✅  |     |     |     | ✅  |     |
| `transformation_secondary:create`        | Crear lote de transformación secundaria              |     | ✅  |     |     |     | ✅  |     |
| `transformation_secondary:process`       | Completar y guardar documentos por etapas de TS      |     | ✅  |     |     |     | ✅  |     |
| `transformation_secondary:generate_qr`   | Generar QR para lote de transformación secundaria    |     | ✅  |     |     |     | ✅  |     |
| `transformation_secondary:view_location` | Ver ubicación de lote de transformación secundaria   |     | ✅  |     |     |     | ✅  |     |
| `dashboard:*`                            | Todos los permisos para dashboard                    |     | ✅  |     |     |     |     |     |
| `dashboard:view`                         | Ver dahboard empresarial.                            |     | ✅  |     |     |     |     |     |

---

## Primer borrador de `PERMISSIONS.ts`

> Ruta sugerida: `src/app/core/auth/permissions.ts`

```ts
// src/app/core/auth/permissions.ts

export const PERMISSIONS = {
  GLOBAL: {
    ALL: '*:*',
  },

  COMPANY: {
    ALL: 'company:*',
  },

  COMMUNITY: {
    ALL: 'community:*',
  },

  PRODUCT: {
    ALL: 'product:*',
  },

  USER: {
    ALL: 'user:*',
  },

  PROFILE: {
    ALL: 'profile:*',
  },

  FORM: {
    ALL: 'form:*',
  },

  PROJECT: {
    ALL: 'project:*',

    READ: 'project:read',
    CREATE: 'project:create',
    UPDATE: 'project:update',

    APPROVE_PMF: 'project:approve_pmf',
    UPLOAD_MAP: 'project:upload_map',
    ACTIVATE_INVENTORY: 'project:activate_inventory',
    APPROVE_INVENTORY: 'project:approve_inventory',
    UPLOAD_UMF_MAP: 'project:upload_umf_map',
    ACTIVATE_PMF_GENERATION: 'project:activate_pmf_generation',
    INSERT_CALCULATED_COLUMNS: 'project:insert_calculated_columns',

    VIEW_DOCUMENTS: 'project:view_documents',
    REGISTER_DOCUMENTS: 'project:register_documents',

    DOWNLOAD_PDF: 'project:download_pdf',
    SEND_PDF: 'project:send_pdf',
    UPLOAD_PMF_APPROVAL_DOCS: 'project:upload_pmf_approval_docs',

    ACTIVATE_COLLECTION: 'project:activate_collection',
    CREATE_COLLECTION_ORDERS: 'project:create_collection_orders',
    GENERATE_PAYMENT_ORDERS: 'project:generate_payment_orders',

    APPROVE_COLLECTION_RECEPTION: 'project:approve_collection_reception',
    PROCESS_COLLECTION: 'project:process_collection',
    PRIMARY_TRANSFORMATION: 'project:primary_transformation',
    ISSUE_PRODUCTION_LOT: 'project:issue_production_lot',

    APPROVE_LOT_RECEPTION: 'project:approve_lot_reception',
    REGISTER_LOT_DELIVERY: 'project:register_lot_delivery',
    APPROVE_FINISHED_LOT_RECEPTION: 'project:approve_finished_lot_reception',
  },

  COLLECTOR: {
    ALL: 'collector:*',
  },

  BRIGADE: {
    ALL: 'brigade:*',
  },

  ACTIVITY: {
    ALL: 'activity:*',
  },

  PAYMENT: {
    ALL: 'payment:*',
  },

  COLLECTION: {
    APPROVE_REQUESTS: 'collection:approve_requests',
  },
} as const;

// (Opcional) tipo útil si luego quieres tipar inputs en directiva/servicios
export type Permission =
  (typeof PERMISSIONS)[keyof typeof PERMISSIONS][keyof (typeof PERMISSIONS)[keyof typeof PERMISSIONS]];
```

---
