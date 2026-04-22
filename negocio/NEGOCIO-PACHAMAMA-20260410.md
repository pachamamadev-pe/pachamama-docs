# Resumen Ejecutivo — Infraestructura Digital para Pachamama

**Proyecto:** Pachamama — REORI CORP S.A.C.
**Preparado por:** Equipo de Arquitectura Cloud
**Fecha:** 10 de Abril de 2026
**Versión:** 1.0
**Audiencia:** Dirección General / Gerencia

---

## Resumen para la Dirección

El sistema Pachamama opera actualmente con tecnología dispersa en cinco proveedores distintos, lo que genera lentitud entre sus componentes, mayor riesgo de seguridad y una facturación fragmentada difícil de controlar. El equipo técnico evaluó tres formas de consolidar toda la infraestructura en un único proveedor cloud de nivel empresarial, con diferente equilibrio entre velocidad, costo y riesgo. La opción recomendada —migración progresiva por etapas— requiere una inversión mensual de **USD 334.94** (~S/ 1,260) y puede completarse en su totalidad en **10 semanas a partir de Junio 2026**. Esta consolidación permitirá a Pachamama escalar de manera ordenada hacia un modelo de múltiples clientes (SaaS) sin comprometer la continuidad del servicio actual.

---

## ¿Qué se está construyendo?

### El problema que se resuelve

Hoy, los servicios digitales de Pachamama —la aplicación móvil, el panel de administración, las bases de datos y los procesos automáticos— funcionan sobre infraestructura distribuida en cinco empresas tecnológicas distintas. Esto es habitual durante el desarrollo inicial de un producto (etapa MVP), pero genera tres problemas concretos al crecer:

1. **Lentitud acumulada**: cuando el usuario realiza una acción, los sistemas deben "hablar" entre sí cruzando proveedores en distintos países. Esto añade tiempos de espera de hasta 200 milisegundos en cada comunicación interna, equivalente a que un empleado tenga que llamar a otro en vez de hablarle al lado.

2. **Riesgo de seguridad**: cada proveedor maneja sus propias claves de acceso. Con cinco proveedores, hay cinco puntos donde una credencial puede ser comprometida. No existe hoy un único lugar donde revocar o auditar todos los accesos.

3. **Escala imposible sin reestructuración**: el modelo de negocio proyecta atender a 10 clientes empresariales con 100 usuarios cada uno. La infraestructura actual no fue diseñada para eso; la arquitectura propuesta sí lo está.

### Qué se propone y quiénes se benefician

Se propone **migrar todos los servicios a una única plataforma cloud de nivel empresarial**, eliminando las dependencias externas de cómputo y datos. Al completar la migración:

- Los tiempos de respuesta interna caen de hasta 200 ms a menos de 5 ms (equivalente a pasar de comunicación por correo a comunicación cara a cara).
- Todas las claves y contraseñas estarán en una única bóveda digital, auditable y con rotación automática.
- La aplicación escalará automáticamente según la demanda sin intervención del equipo técnico.
- La empresa recibirá **una sola factura mensual** en lugar de cinco.

Los beneficiarios directos son los supervisores y brigadistas que usan la app en campo, los administradores que gestionan el panel web, y el equipo de TI que deja de gestionar múltiples consolas de administración.

---

## Las Opciones Disponibles

> Las tres opciones llevan a **la misma plataforma final**. La diferencia está en cómo se ejecuta la transición: a qué velocidad, con qué nivel de riesgo y cuántas semanas se pagan costos en paralelo.

---

### Opción A: Migración Progresiva por Etapas ⭐ Recomendada

**En una línea:** Mover los servicios en cuatro grupos ordenados, validando cada uno antes de avanzar al siguiente. Si algo falla, se puede retroceder en minutos.

| Dimensión | Detalle |
|---|---|
| Inversión mensual (estado final) | USD 334.94 / ~S/ 1,261 |
| Inversión anual (estado final) | USD 4,019 / ~S/ 15,132 |
| Costo adicional durante la transición | USD 150–250 totales (servicios en paralelo ~8 semanas) |
| Tiempo de puesta en marcha | 10 semanas (Junio – Agosto 2026) |
| Nivel de riesgo | **Bajo** |
| Disponibilidad del servicio | 99.5% (máximo 43.8 horas de parada al año) |
| ¿Para qué tipo de empresa es ideal? | Equipos pequeños (1–2 personas técnicas), producto en producción activa, primera migración de esta escala |

**Lo que el negocio gana:**
- La transición ocurre sin interrupciones visibles para los usuarios finales.
- El equipo aprende la nueva plataforma de forma gradual, reduciendo errores.
- En cada etapa hay un "botón de retroceso" disponible: si algo falla, se revierte en minutos sin afectar a los usuarios.
- Ventanas de corte de solo ~30 minutos por etapa, en horarios de baja actividad.

**Lo que el negocio asume:**
- Es la opción más lenta (10 semanas en total).
- Durante ~8 semanas se pagan dos infraestructuras en paralelo (la actual y la nueva), con un costo adicional de USD 150–250 en ese período.

---

### Opción B: Migración por Área de Negocio

**En una línea:** Mover un área completa (identidad, sincronización, notificaciones, trazabilidad) de principio a fin antes de empezar con la siguiente.

| Dimensión | Detalle |
|---|---|
| Inversión mensual (estado final) | USD 334.94 / ~S/ 1,261 |
| Inversión anual (estado final) | USD 4,019 / ~S/ 15,132 |
| Costo adicional durante la transición | USD 100–200 totales (~6 semanas en paralelo) |
| Tiempo de puesta en marcha | 9 semanas (Junio – Agosto 2026) |
| Nivel de riesgo | **Medio** |
| Disponibilidad del servicio | 99.5% (máximo 43.8 horas de parada al año) |
| ¿Para qué tipo de empresa es ideal? | Equipos con 2–3 personas técnicas y experiencia previa en migraciones de bases de datos |

**Lo que el negocio gana:**
- Cada área queda completamente operativa en la nueva plataforma antes de avanzar, lo que facilita las pruebas funcionales por módulo.
- Menor superposición de costos que la Opción A.

**Lo que el negocio asume:**
- Las áreas de negocio tienen dependencias entre sí: si la primera (identidad + base de datos principal) falla, todo lo demás queda bloqueado.
- Requiere más coordinación técnica entre módulos que la Opción A.
- El equipo actual puede estar al límite de capacidad para ejecutarla sin apoyo adicional.

---

### Opción C: Migración Acelerada (Corte Único)

**En una línea:** Preparar todo en 3 semanas y ejecutar un único corte programado de 4–6 horas un fin de semana, pasando del sistema actual al nuevo de una sola vez.

| Dimensión | Detalle |
|---|---|
| Inversión mensual (estado final) | USD 334.94 / ~S/ 1,261 |
| Inversión anual (estado final) | USD 4,019 / ~S/ 15,132 |
| Costo adicional durante la transición | USD 50–100 totales (~3 semanas en paralelo) |
| Tiempo de puesta en marcha | 4 semanas (posible inicio Junio 2026) |
| Nivel de riesgo | **Alto** |
| Disponibilidad del servicio | 99.5% (máximo 43.8 horas de parada al año) |
| ¿Para qué tipo de empresa es ideal? | Equipos con experiencia sólida en migraciones cloud, o cuando hay presión presupuestaria para reducir al mínimo los costos de transición |

**Lo que el negocio gana:**
- Menor período pagando infraestructura doble (~3 semanas).
- El equipo se enfoca en un sprint corto e intenso.
- La nueva plataforma está operativa en menos de un mes.

**Lo que el negocio asume:**
- **Máximo riesgo**: un problema durante el corte afecta todos los servicios a la vez (app móvil, panel web, bases de datos, notificaciones).
- Se requiere comunicar anticipadamente a todos los usuarios una ventana de indisponibilidad programada de 4–6 horas.
- El plan de retroceso en caso de fallo es significativamente más complejo de ejecutar bajo presión.
- Requiere experiencia técnica avanzada en migraciones cloud; el equipo actual puede necesitar refuerzo externo.

---

## Comparación de Opciones

| Criterio de Negocio | Opción A — Progresiva ⭐ | Opción B — Por Área | Opción C — Corte Único |
|---|---|---|---|
| Inversión mensual (final) | USD 334.94 | USD 334.94 | USD 334.94 |
| Semanas pagando doble | 8 semanas | 6 semanas | 3 semanas |
| Velocidad de lanzamiento | 10 semanas | 9 semanas | 4 semanas |
| Riesgo operativo | **Bajo** | Medio | Alto |
| Impacto en usuarios durante transición | Imperceptible | Mínimo (< 1h/módulo) | 4–6 h de corte total |
| Capacidad de revertir si hay problemas | Alta (por etapa) | Media (por módulo) | Baja (retroceso complejo) |
| Capacidad de crecimiento post-migración | Igual para las 3 | Igual para las 3 | Igual para las 3 |
| Exigencia al equipo técnico | Manejable | Moderada | Alta / requiere refuerzo |
| **Puntaje ejecutivo (1–5)** | **5** | **3** | **2** |

---

## ¿Qué implica para el equipo y los procesos?

### Personal y capacitación
- La migración puede ejecutarse con el equipo técnico actual (1–2 personas) bajo la Opción A recomendada.
- El equipo necesitará familiarizarse con la consola de administración del nuevo proveedor cloud —estimado 1–2 días de autoestudio cubiertos durante la ejecución del proyecto.
- No se requiere contratar personal adicional para la Opción A.
- Los servicios de autenticación (Firebase) y mensajería WhatsApp (Twilio) **no cambian**: los usuarios no notarán diferencia en cómo inician sesión o reciben códigos OTP.

### Procesos del negocio
- La aplicación móvil y el panel web continuarán funcionando con normalidad durante toda la transición bajo la Opción A.
- Las notificaciones push y la sincronización sin conexión a internet (modo offline) se mantienen sin cambios para el usuario final.
- El único cambio visible para el equipo de administración será la nueva URL del panel durante la Wave 1, que es el primer paso de cero riesgo.

### Operación diaria post-migración
- El equipo de TI pasará de administrar cinco plataformas independientes a administrar **una sola consola centralizada**.
- Las alertas de sistema (errores, carga, costos) llegarán a un único panel, eliminando la necesidad de revisar múltiples dashboards.
- Los despliegues de nuevas versiones de la aplicación serán automáticos: cuando el equipo suba cambios al repositorio de código, el sistema se actualiza solo sin pasos manuales.

---

## Cronograma en Lenguaje de Negocio

> Línea de tiempo bajo la **Opción A Recomendada**, con inicio el 1 de Junio de 2026.

```
Junio (Semanas 1–2):   Preparación y gobierno
                        → Se configura la nueva plataforma cloud con su sistema
                          de gestión de accesos y contraseñas centralizado.
                        → El sitio web de administración y el landing page migran
                          al nuevo proveedor. Cero riesgo: los datos no se tocan.

Junio–Julio (Semanas 3–5):  Migración de bases de datos
                        → Las bases de datos principales (registros, actividades,
                          notificaciones, trazabilidad) se replican en la nueva
                          plataforma y se validan en paralelo antes de hacer el
                          cambio definitivo. Sin corte de servicio.

Julio (Semanas 6–8):   Migración de aplicaciones backend
                        → Los cuatro servidores de la aplicación se mueven a la nueva
                          plataforma de forma gradual: primero el 10% del tráfico,
                          luego el 50%, finalmente el 100%. Si hay algún problema,
                          se revierte en minutos ajustando una variable de entorno.

Agosto (Semanas 9–10): Cierre y baja de proveedores antiguos
                        → Se confirma la estabilidad durante 72 horas con el 100%
                          del tráfico en la nueva plataforma.
                        → Los servicios antiguos se ponen en stand-by 14 días como
                          red de seguridad; luego se eliminan y se confirma el costo
                          mensual final.
```

---

## Riesgos del Negocio y Plan de Respuesta

| Riesgo | Probabilidad | Impacto en el negocio | ¿Cómo se gestiona? |
|---|---|---|---|
| La base de datos principal no migra correctamente y algunos registros históricos no quedan disponibles de inmediato | Baja | Alto | Se ejecuta una validación de integridad contando registros antes y después. La base de datos original permanece activa dos semanas adicionales como respaldo. |
| El sistema de registros geoespaciales (mapa de actividades) no funciona igual en la nueva plataforma | Baja | Alto | Se valida específicamente durante la etapa de bases de datos, antes de cualquier corte. Si no pasa la prueba, se mantiene en el proveedor original hasta resolver la compatibilidad. |
| Los servidores de la aplicación tardan más de lo esperado en responder durante las primeras horas en la nueva plataforma (arranque en frío) | Media | Medio | Se configura al menos una instancia siempre activa para los módulos más críticos. Costo adicional estimado: ~USD 20/mes. |
| El costo mensual final supera el estimado si la carga de usuarios es mayor a la proyectada | Baja | Medio | Se configuran alertas automáticas a USD 250/mes (aviso) y USD 400/mes (crítico), con revisión semanal de los contadores de uso. |
| El equipo técnico no cuenta con los permisos necesarios en la plataforma cloud para aprovisionar ciertos recursos a tiempo | Media | Bloqueante para la etapa afectada | Solicitar las cuotas de capacidad con una semana de anticipación a cada etapa. Identificado en el plan y no depende de terceros. |

---

## Costo Total de Propiedad

### Inversión mensual en estado operativo final

| Componente | Costo mensual USD |
|---|---|
| Servidores de aplicación (4 módulos backend) | USD 72.12 |
| Base de datos relacional principal (registros y actividades) | USD 144.66 |
| Base de datos documental (notificaciones y trazabilidad) | USD 15.00 |
| Caché de sesión y datos geoespaciales | USD 55.00 |
| Mensajería interna del sistema | USD 30.00 |
| Almacenamiento de archivos (fotos, documentos) | USD 4.16 |
| Sitios web (panel admin + landing) | USD 9.00 |
| Procesos automáticos (SAS + Trazabilidad) | USD 5.00 |
| Seguridad, monitoreo y logs | ~USD 9.00 |
| **Total mensual estimado** | **~USD 334.94** |

### Perspectiva de inversión a 12 y 36 meses

| Horizonte | Inversión total estimada |
|---|---|
| 12 meses (primer año) | **USD ~4,350** *(incluye ~USD 200–250 adicionales de transición)* |
| 36 meses | **USD ~11,700** *(con ahorro de ~USD 600 en años 2–3 al activar reservas de capacidad)* |

> **¿Qué incluye este costo?**
> Toda la infraestructura cloud necesaria para operar Pachamama con hasta 1,000 usuarios concurrentes: servidores, bases de datos, almacenamiento, mensajería, seguridad y observabilidad.
>
> **¿Qué NO incluye?**
> Horas de trabajo del equipo técnico para ejecutar la migración, licencias de servicios externos que se mantienen sin cambio (autenticación y mensajería WhatsApp), ni soporte premium del proveedor cloud. Si se desea soporte técnico con SLA del proveedor, estimar un costo adicional de USD 29–100/mes según el plan.

### Comparativa: costo actual vs. costo objetivo

| Situación | Costo mensual estimado |
|---|---|
| Infraestructura actual (5 proveedores) | USD 87–103/mes |
| Infraestructura objetivo (consolidada) | USD 334.94/mes |
| Incremento mensual | +USD 232–248/mes |

> **¿Por qué sube el costo si hay una consolidación?** El costo actual de USD 87–103/mes corresponde en su mayoría a planes básicos o gratuitos con limitaciones significativas (sin alta disponibilidad, sin SLA empresarial, sin escalabilidad automática). La nueva infraestructura es de grado productivo: la base de datos principal opera en un servidor dedicado con respaldo automático, Redis tiene replicación activa para alta disponibilidad, y los servidores escalan automáticamente. Es el costo de pasar de un MVP a una plataforma lista para clientes empresariales.

---

## Recomendación

El equipo técnico recomienda la **Opción A — Migración Progresiva por Etapas**, con inicio el **1 de Junio de 2026**.

Es la opción más conveniente para Pachamama por tres razones de negocio:

1. **Mínimo riesgo para el servicio activo.** Al mover los componentes en cuatro etapas con validación en cada paso, el riesgo de afectar a los usuarios es prácticamente nulo. Esto protege la reputación del producto en un momento de crecimiento.

2. **Accesible para el equipo actual.** No requiere contratar personal adicional ni experiencia avanzada previa en migraciones cloud. El equipo de 1–2 personas puede ejecutarla de forma ordenada aprendiendo progresivamente.

3. **Fundación correcta para el modelo SaaS.** Una vez completada, la plataforma estará lista para incorporar nuevos clientes empresariales sin rediseño adicional: escalado automático, seguridad centralizada, observabilidad unificada y una sola factura mensual.

El mayor componente de costo incremental (USD ~145/mes de la base de datos principal) responde al reemplazo de un plan básico sin garantías por un servidor dedicado con respaldo automático horario, replicación y recuperación ante fallas. Este es el componente irrenunciable de la arquitectura para un producto en producción real.

---

## Próximos Pasos y Decisiones Requeridas

| # | Acción | Responsable | Fecha sugerida |
|---|---|---|---|
| 1 | Aprobar la Opción A como estrategia de migración | Gerencia General | 18 de Abril 2026 |
| 2 | Aprobar presupuesto mensual de USD 334.94 (~S/ 1,261) para infraestructura cloud | Gerencia Financiera | 18 de Abril 2026 |
| 3 | Aprobar presupuesto adicional de transición de USD 200–250 (pago único) | Gerencia Financiera | 18 de Abril 2026 |
| 4 | Designar al responsable técnico de la migración y confirmar disponibilidad desde Junio 2026 | CTO / Gerencia TI | 25 de Abril 2026 |
| 5 | Confirmar acceso del equipo técnico a la suscripción corporativa cloud con permisos suficientes | CTO / Gerencia TI | 10 de Mayo 2026 |
| 6 | Aprobar comunicado interno a usuarios piloto sobre la ventana de mantenimiento (Wave 3, Julio 2026) | Gerencia de Producto | 20 de Mayo 2026 |

---

## Glosario Ejecutivo

| Término técnico | Qué significa para el negocio |
|---|---|
| **API / Backend** | El motor invisible que procesa las solicitudes de la aplicación: cuando el usuario guarda un registro, el backend lo recibe, valida y almacena. |
| **App Insights / Log Analytics** | Panel de control y alertas del estado del sistema; equivalente al panel de instrumentos de un avión. |
| **Azure Cache for Redis** | Memoria temporal que acelera las respuestas del sistema; reduce la carga sobre la base de datos para consultas frecuentes. |
| **Azure Container Apps** | Servidor en la nube que ejecuta las aplicaciones de Pachamama; se expande o contrae automáticamente según la cantidad de usuarios conectados. |
| **Azure Functions / Serverless** | Tareas automáticas que solo consumen recursos (y solo generan costo) cuando se ejecutan; por ejemplo, generar un enlace de acceso a un archivo o sincronizar un evento de trazabilidad. |
| **Azure Static Web Apps** | Servidor especializado en alojar sitios web; reemplaza al proveedor actual del panel de administración y del landing page. |
| **Blob Storage** | Repositorio seguro de archivos y documentos en la nube; donde se almacenan las fotos de campo, documentos de actividades y archivos de onboarding. |
| **CI/CD Pipeline** | Proceso automatizado que publica nuevas versiones de la aplicación sin intervención manual; cuando el equipo sube cambios al repositorio, el sistema se actualiza solo. |
| **Cosmos DB** | Base de datos especializada en notificaciones y registros de trazabilidad; flexible y de alta velocidad para consultas no estructuradas. |
| **Dyno (Heroku)** | Nombre que el proveedor actual usa para referirse a un servidor de aplicación; equivale a lo que Azure llama Container App. |
| **Firebase Auth / FCM** | Servicio externo de autenticación de usuarios y envío de notificaciones push; se mantiene sin cambios —los usuarios seguirán iniciando sesión igual y recibiendo notificaciones igual. |
| **Key Vault** | Bóveda digital centralizada que guarda todas las contraseñas y claves de acceso del sistema; ningún secreto queda escrito en el código fuente. |
| **Managed Identity / RBAC** | Sistema que permite a los componentes del sistema identificarse y acceder entre sí sin contraseñas explícitas; equivalente a que cada empleado tenga su credencial corporativa en vez de compartir una contraseña genérica. |
| **MongoDB / Cosmos DB API MongoDB** | Base de datos documental usada para notificaciones y trazabilidad; almacena información de estructura flexible, como el historial de eventos de una actividad. |
| **Offline-first** | La aplicación funciona sin conexión a internet y sincroniza los datos cuando la conexión se recupera; diseñado para trabajo en campo con cobertura intermitente. |
| **Pay-as-you-go** | Modelo de pago en el que solo se factura lo que se consume; sin compromisos mínimos mensuales fijos por servicio. |
| **PostGIS / Geoespacial** | Extensión de la base de datos que permite almacenar y consultar coordenadas geográficas, rutas y áreas; esencial para el mapa de actividades de Pachamama. |
| **PostgreSQL Flexible Server** | Base de datos relacional principal de Pachamama; almacena usuarios, actividades, registros de campo y toda la información estructurada del sistema. |
| **Reserved Instances** | Descuento de ~20–30% al comprometerse a usar un recurso por 1 año prepagado; aplicable a los componentes más costosos (base de datos y caché) a partir del segundo año. |
| **Resource Group** | Carpeta organizadora dentro de la plataforma cloud que agrupa todos los recursos de Pachamama para facilitar la gestión, facturación y control de accesos. |
| **RTO / RPO** | RTO: cuánto tarda el sistema en recuperarse ante una falla (objetivo: máx. 4 horas). RPO: cuántos datos se podrían perder en el peor caso (objetivo: máx. 1 hora de actividad). |
| **SaaS (Software as a Service)** | Modelo de negocio en el que Pachamama ofrece su plataforma a múltiples clientes empresariales, cada uno con sus propios datos aislados, sobre la misma infraestructura compartida. |
| **Service Bus** | Sistema de mensajería interna del sistema; permite que los módulos de la aplicación se comuniquen de forma asíncrona y confiable sin bloquearse mutuamente. |
| **SLA 99.5%** | El sistema estará disponible al menos 99.5% del tiempo, equivalente a un máximo de 43.8 horas de parada no planificada al año. |
| **Traffic Splitting** | Técnica de migración que redirige gradualmente el tráfico de usuarios del sistema antiguo al nuevo (10% → 50% → 100%), permitiendo revertir en minutos si algo falla. |
| **Twilio** | Proveedor externo de mensajería WhatsApp usado para enviar códigos de verificación (OTP); se mantiene sin cambios. |
| **VNet / Red Privada** | Red interna y privada que conecta todos los componentes de Pachamama dentro de la plataforma cloud; ningún componente queda expuesto directamente a internet. |
| **Wave / Ola** | Nombre que el equipo técnico da a cada etapa de la migración progresiva; equivale a una fase del proyecto con un conjunto definido de actividades y criterios de éxito. |
