---
name: verificar-referencias
description: "Skill para verificar la autenticidad de referencias bibliográficas en trabajos de investigación. Detecta referencias inexistentes (hallucinations de IA), títulos mal citados, autores incorrectos y DOIs inválidos. Acepta archivos .docx, .pdf o texto pegado. Consulta CrossRef API y OpenAlex API (ambas gratuitas, sin API key). Genera un informe Markdown con semáforo de verificación por referencia: VERIFICADA / POSIBLE / SOSPECHOSA / NO ENCONTRADA."
argument-hint: "Archivo .docx o .pdf con el trabajo de investigación, o texto con la lista de referencias"
---

# Verificar Referencias Bibliográficas

Analiza cada referencia bibliográfica de un trabajo académico y verifica si realmente existe en bases de datos científicas públicas (CrossRef, OpenAlex, Semantic Scholar).

**Caso de uso principal:** detectar referencias inventadas por IA (hallucinations), errores en títulos, autores o años, y DOIs que no resuelven.

---

## Principios de Operación

1. **Sin API key** — usa CrossRef y OpenAlex (gratuitas, sin registro).
2. **No solicita PDF completo** — solo verifica metadatos: título, autores, año, revista, DOI.
3. **Nivel de confianza por referencia** — semáforo de 4 niveles con porcentaje de coincidencia.
4. **Respeta límites de velocidad** — pausa 0.5s entre llamadas (CrossRef polite pool).
5. **Entregable Markdown** — `REFS-<NOMBRE_ARCHIVO>-<YYYYMMDD>.md` en la carpeta `verificaciones/`.

---

## Flujo de Trabajo

### Paso 1 — Recibir el insumo

| Formato | Acción |
|---------|--------|
| Archivo `.docx` | Ejecutar `python verificar_referencias.py --file archivo.docx` |
| Archivo `.pdf` | Ejecutar `python verificar_referencias.py --file archivo.pdf` |
| Texto pegado | Guardar en `.txt` temporal y ejecutar con `--file` |
| Lista de referencias en chat | Extraerlas y pasarlas como texto al script |

Si el usuario pega las referencias directamente en el chat, copiarlas a un archivo temporal `refs_temp.txt` y procesar.

### Paso 2 — Instalar dependencias

```bash
pip install python-docx requests pymupdf
```

Si `pymupdf` falla (Windows), alternativa: `pip install pdfminer.six`

### Paso 3 — Ejecutar el script

```bash
python verificar_referencias.py --file "mi_tesis.docx"
```

Opciones disponibles:

| Opción | Default | Descripción |
|--------|---------|-------------|
| `--file` | requerido | Ruta al archivo `.docx`, `.pdf` o `.txt` |
| `--section` | auto | Nombre de la sección de referencias (ej: "Bibliografía") |
| `--email` | anon | Email para polite pool de CrossRef (opcional, mejora velocidad) |
| `--out` | `verificaciones/` | Carpeta de salida del informe |
| `--min-score` | 60 | Porcentaje mínimo para considerar una referencia "POSIBLE" |

### Paso 4 — Interpretar el informe

Cada referencia recibe un estado:

| Estado | Color | Significado |
|--------|-------|-------------|
| ✅ VERIFICADA | Verde | Coincidencia ≥ 85% en título + al menos 1 autor + año ±1 |
| 🟡 POSIBLE | Amarillo | Coincidencia 60–84% o datos parciales encontrados |
| 🔴 SOSPECHOSA | Rojo | Encontrado pero con discrepancias significativas (año, autores, revista) |
| ❌ NO ENCONTRADA | Gris | Ninguna fuente retorna resultados relevantes |

---

## El Script

El script `verificar_referencias.py` está en `.github/skills/verificar-referencias/verificar_referencias.py`.

Copiarlo al directorio de trabajo antes de ejecutar, o ejecutarlo con ruta absoluta.

---

## Formato del Informe de Salida

```markdown
# Verificación de Referencias Bibliográficas
**Archivo analizado:** mi_tesis.docx  
**Fecha:** 2026-04-10  
**Total referencias:** 24  
**Verificadas:** 18 (75%)  
**Posibles:** 3 (12.5%)  
**Sospechosas:** 1 (4.2%)  
**No encontradas:** 2 (8.3%)

---

## Resumen Ejecutivo
[párrafo con interpretación de los resultados]

---

## Detalle por Referencia

### 1. ✅ VERIFICADA (96%)
**Referencia original:**
> García, A., & López, M. (2021). Machine learning in agriculture. *Nature Food*, 2(4), 199–208.

**Encontrada en:** CrossRef  
**DOI verificado:** https://doi.org/10.1038/s43016-021-00258-8  
**Título en fuente:** Machine learning in agriculture (exact match)  
**Autores en fuente:** García, A.; López, M. ✓  
**Año en fuente:** 2021 ✓  
**Revista en fuente:** Nature Food ✓

---

### 3. ❌ NO ENCONTRADA
**Referencia original:**
> Smith, J. (2023). Deep learning for crop yield prediction. *Journal of Agricultural AI*, 15(2), 45–67.

**Búsqueda en CrossRef:** 0 resultados relevantes  
**Búsqueda en OpenAlex:** título no encontrado  
**Búsqueda en Semantic Scholar:** no encontrado  
**⚠️ Posibles causas:** título incorrecto, revista inexistente, referencia generada por IA
```

---

## Reglas Especiales

```
SI la referencia tiene DOI → verificar primero con https://doi.org/{DOI}
     Si el DOI resuelve → VERIFICADA automáticamente (sin buscar por título)
     Si el DOI no resuelve → marcar como SOSPECHOSA y buscar por título

SI el año de la referencia es > año actual → marcar como SOSPECHOSA

SI la revista no aparece en CrossRef pero sí en Google Scholar → marcar POSIBLE
     (no hacer scraping de Google Scholar; solo informar al usuario)

SI hay más de 30 referencias → procesar en lotes de 10 con pausa entre lotes

SI el idioma de las referencias es español → usar también el campo "alternative-title"
     en OpenAlex para títulos traducidos

SI el score CrossRef es < 30 en todos los resultados → intentar con OpenAlex
SI el score OpenAlex también es bajo → intentar con Semantic Scholar
SI los 3 fallan → NO ENCONTRADA
```

---

## APIs Utilizadas

### CrossRef
```
GET https://api.crossref.org/works?query.title={TITULO}&query.author={AUTOR}&rows=5
Headers: User-Agent: VerificarRefs/1.0 (mailto:{EMAIL})
```
Score de relevancia nativo (0–100). Campo `score` en la respuesta.

### OpenAlex
```
GET https://api.openalex.org/works?search={TITULO}&per-page=3
```
Sin autenticación. Retorna `relevance_score` y metadatos completos.

### Semantic Scholar
```
GET https://api.semanticscholar.org/graph/v1/paper/search?query={TITULO}&fields=title,authors,year,externalIds,venue&limit=3
```
Fallback cuando CrossRef y OpenAlex no retornan resultados.

### Resolución de DOI
```
HEAD https://doi.org/{DOI}
```
Si retorna 200/301/302 → DOI válido y resoluble.

---

## Integración con Otros Skills

| Situación | Skill a invocar |
|----------|----------------|
| El trabajo está en `.docx` | `docx` para extraer texto si python-docx falla |
| El trabajo está en `.pdf` | `pdf` para extraer texto |
| El usuario quiere el informe en Word | `docx` para convertir el `.md` generado |
| El usuario quiere corregir las referencias detectadas | Usar el informe para editar el `.docx` original con skill `docx` |
