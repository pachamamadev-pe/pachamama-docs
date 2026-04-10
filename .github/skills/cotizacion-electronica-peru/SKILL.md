---
name: cotizacion-electronica-peru
description: "Generacion de cotizaciones profesionales de equipos electronicos y de computo para el mercado peruano. Usar cuando el usuario solicite crear una nueva cotizacion, agregar articulos a una cotizacion existente, actualizar precios o condiciones, o generar cualquier documento de cotizacion para clientes. Empresa vendedora fija: TechPeru SAC, RUC 10482686929. Soporta moneda soles (S/.) y dolares (USD) con tipo de cambio ingresado por el usuario. Precios incluyen IGV (18%). Genera documentos Markdown como salida."
---

# Cotizacion Electronica Peru

Genera cotizaciones profesionales de equipos electronicos y computo para GRUPO DO SANTOS INVERSIONES GENERALES E.I.R.L., orientadas al mercado peruano.

## Datos de la Empresa Vendedora (fijos)

- **Razon Social**: GRUPO DO SANTOS INVERSIONES GENERALES E.I.R.L.
- **RUC**: 20609820544
- **Pais**: Peru

## Flujo: Nueva Cotizacion

Recopilar datos en este orden. Preguntar solo lo necesario; si el usuario ya proporcionó datos, no re-preguntar.

### 1. Datos del cliente (obligatorios)
Solicitar:
- Razon social del cliente
- RUC del cliente (11 digitos)
- Direccion (opcional pero recomendada)
- Contacto, email y/o telefono (opcional)

### 2. Numero y fecha
- Proponer numero de cotizacion en formato `COT-YYYY-NNN` (e.g., `COT-2026-001`); incrementar NNN si hay cotizaciones previas en la sesion
- Fecha: usar la fecha actual
- Validez: 7 dias calendario (estandar Peru); ajustar si el usuario indica otra

### 3. Moneda
- Preguntar: S/. (Soles) o $ (Dolares USD)
- Si es USD: solicitar tipo de cambio (TC) del dia (e.g., S/. 3.75)
- Guardar TC para mostrar equivalencia en soles al final del documento

### 4. Articulos
Para cada articulo, consultar referencias/especificaciones-tecnicas.md segun la categoria del producto y recopilar:
- Categoria del producto
- Marca y modelo
- Especificaciones tecnicas clave (segun categoria)
- Cantidad
- Precio unitario **con IGV incluido** en la moneda seleccionada

Continuar agregando articulos hasta que el usuario confirme que termino.

### 5. Condiciones comerciales
Solicitar si no se especificaron:
- Forma de pago (e.g., Contado, 50% adelanto + 50% contra entrega, Credito 30 dias)
- Tiempo de entrega estimado (e.g., 3-5 dias habiles)
- Garantia (e.g., 12 meses con el fabricante)

### 6. Generar documento
Aplicar la plantilla de referencias/plantilla-cotizacion.md y generar el documento Markdown completo.

---

## Flujo: Agregar Articulos a Cotizacion Existente

1. Identificar la cotizacion (por numero o contenido en el historial de conversacion)
2. Agregar los nuevos articulos al final de la tabla
3. Recalcular subtotal neto, IGV y total
4. Si la moneda es USD, recalcular la equivalencia en soles con el TC original
5. Regenerar el documento Markdown completo y actualizado

---

## Calculo de Totales (Precios con IGV incluido)

Los precios unitarios ya incluyen IGV (18%). Los totales se calculan asi:

| Concepto | Formula |
|---|---|
| Total bruto | suma de (precio_unitario x cantidad) |
| Subtotal neto (sin IGV) | Total bruto / 1.18 |
| IGV (18%) | Total bruto - Subtotal neto |
| **TOTAL** | Total bruto |

Si la moneda es USD, agregar al final:
- `Tipo de cambio: S/. {TC}`
- `Equivalente en soles: S/. {TOTAL * TC}`

---

## Referencias

- **Plantilla y formato del documento**: Ver [references/plantilla-cotizacion.md](references/plantilla-cotizacion.md)
- **Especificaciones tecnicas por categoria**: Ver [references/especificaciones-tecnicas.md](references/especificaciones-tecnicas.md) — cargar al inicio de cada cotizacion para saber que datos pedir segun la categoria del producto
