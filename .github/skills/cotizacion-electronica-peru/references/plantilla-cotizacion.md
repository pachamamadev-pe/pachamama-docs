# Plantilla de Cotizacion

## Estructura del documento Markdown

Usar exactamente esta estructura al generar el documento. Reemplazar los valores entre `{llaves}`.

---

```markdown
# COTIZACION DE EQUIPOS {COT-YYYY-NNN}

---

## DATOS DEL VENDEDOR

| | |
|---|---|
| **Empresa** | GRUPO DO SANTOS INVERSIONES GENERALES E.I.R.L. |
| **RUC** | 20609820544 |
| **Fecha** | {DD/MM/YYYY} |
| **Validez** | {N} dias calendario |

---

## DATOS DEL CLIENTE

| | |
|---|---|
| **Razon Social** | {Razon social del cliente} |
| **RUC** | {RUC del cliente} |
| **Direccion** | {Direccion o — si no se proporciono} |
| **Contacto** | {Nombre, email, telefono o — si no se proporciono} |

---

## DETALLE DE ARTICULOS

| N° | Descripcion | Marca / Modelo | Especificaciones | Cant. | P. Unit. ({MONEDA} c/IGV) | Total ({MONEDA}) |
|---|---|---|---|---|---|---|
| 1 | {Descripcion del producto} | {Marca} {Modelo} | {Specs clave} | {Cant} | {P.Unit} | {Total} |
| 2 | {Descripcion del producto} | {Marca} {Modelo} | {Specs clave} | {Cant} | {P.Unit} | {Total} |

---

## RESUMEN ECONOMICO

| Concepto | {MONEDA} |
|---|---|
| Subtotal neto (sin IGV) | {Total bruto / 1.18} |
| IGV (18%) | {Total bruto - Subtotal neto} |
| **TOTAL** | **{Total bruto}** |

<!-- Solo si la moneda es USD: -->
| Tipo de cambio | S/. {TC} |
| Equivalente en soles | S/. {TOTAL * TC} |

---

## CONDICIONES COMERCIALES

| | |
|---|---|
| **Forma de pago** | {Contado / Credito 30 dias / 50% adelanto + 50% contra entrega / etc.} |
| **Tiempo de entrega** | {N dias habiles} |
| **Garantia** | {N meses con el fabricante / soporte tecnico incluido} |
| **Moneda** | {Soles (S/.) / Dolares Americanos (USD)} |

---

## NOTAS Y OBSERVACIONES

{Si hay notas adicionales, listarlas aqui. Si no hay, omitir esta seccion o escribir "Ninguna."}

---

*Cotizacion generada por GRUPO DO SANTOS INVERSIONES GENERALES E.I.R.L. — Todos los precios incluyen IGV (18%)*
```

---

## Reglas de formato

### Moneda
- Soles: usar `S/.` como prefijo y dos decimales. Ejemplo: `S/. 1,250.00`
- Dolares: usar `$` como prefijo y dos decimales. Ejemplo: `$ 340.00`
- Separador de miles: coma (`,`). Separador decimal: punto (`.`)

### Especificaciones en la tabla
- Condensar en una celda. Usar `/` como separador. Ejemplo: `Intel Core i5-1235U / 8GB RAM / 512GB SSD / 15.6" FHD`
- Si las specs son muy largas, abreviar sin perder datos clave

### Numeracion de articulos
- Reiniciar desde 1 en cada cotizacion
- Si se agregan articulos a cotizacion existente, continuar la numeracion

### Calculo de redondeo
- Redondear a 2 decimales en cada operacion
- El IGV = Total bruto - Subtotal neto (nunca calcular IGV por separado por articulo para evitar diferencias de redondeo)

---

## Ejemplo completo (referencia)

```markdown
# COTIZACION DE EQUIPOS COT-2026-001

---

## DATOS DEL VENDEDOR

| | |
|---|---|
| **Empresa** | GRUPO DO SANTOS INVERSIONES GENERALES E.I.R.L. |
| **RUC** | 20609820544 |
| **Fecha** | 08/04/2026 |
| **Validez** | 7 dias calendario |

---

## DATOS DEL CLIENTE

| | |
|---|---|
| **Razon Social** | Corporacion Andina S.A.C. |
| **RUC** | 20456789123 |
| **Direccion** | Av. Javier Prado 1234, San Isidro, Lima |
| **Contacto** | Carlos Quispe — cquispe@andina.com — 987 654 321 |

---

## DETALLE DE ARTICULOS

| N° | Descripcion | Marca / Modelo | Especificaciones | Cant. | P. Unit. (S/. c/IGV) | Total (S/.) |
|---|---|---|---|---|---|---|
| 1 | Laptop Empresarial | HP / EliteBook 640 G10 | Intel Core i5-1335U / 16GB DDR5 / 512GB NVMe / 14" FHD / Win11 Pro | 5 | S/. 3,540.00 | S/. 17,700.00 |
| 2 | Mouse Inalambrico | Logitech / MX Master 3S | Bluetooth + USB, 8000 DPI, ergonomico | 5 | S/. 265.00 | S/. 1,325.00 |
| 3 | Mochila para laptop | Case Logic / DLBP-116 | Hasta 15.6", acolchada, 2 bolsillos | 5 | S/. 185.00 | S/. 925.00 |

---

## RESUMEN ECONOMICO

| Concepto | S/. |
|---|---|
| Subtotal neto (sin IGV) | S/. 16,906.78 |
| IGV (18%) | S/. 3,043.22 |
| **TOTAL** | **S/. 19,950.00** |

---

## CONDICIONES COMERCIALES

| | |
|---|---|
| **Forma de pago** | 50% adelanto, 50% contra entrega |
| **Tiempo de entrega** | 5 dias habiles |
| **Garantia** | 12 meses con el fabricante |
| **Moneda** | Soles (S/.) |

---

*Cotizacion generada por GRUPO DO SANTOS INVERSIONES GENERALES E.I.R.L. — Todos los precios incluyen IGV (18%)*
```
