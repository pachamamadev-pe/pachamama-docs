---
name: convertir_doc_a_markdown
description: Skill para convertir archivos Word (.docx, .doc) o PDF a Markdown sin perder información. Preserva estructura, tablas, listas, estilos de texto, encabezados, links e imágenes. Genera un archivo .md con timestamp en la carpeta indicada o en la raíz del workspace.
---

## Objetivo

Convertir el contenido completo de uno o varios archivos **Word** (.docx / .doc) o **PDF** a formato **Markdown**, preservando toda la información y estructura del documento original.

---

## Escenarios de uso

### Escenario A – Conversión simple (un archivo)
El usuario adjunta un archivo Word o PDF.
- Convertir el contenido íntegro a Markdown.
- Guardar el archivo `.md` resultante con el mismo nombre base del original + timestamp.

### Escenario B – Conversión con carpeta destino especificada
El usuario adjunta un archivo e indica una carpeta destino.
- Convertir e guardar el archivo `.md` en la carpeta especificada.

### Escenario C – Conversión masiva (múltiples archivos)
El usuario adjunta más de un archivo.
- Convertir cada archivo individualmente.
- Generar un archivo `.md` por cada documento.
- Al final, informar un resumen de los archivos generados.

---

## Inputs

- Archivo(s) en formato **PDF**, **.docx** o **.doc** (uno o varios)
- Carpeta destino (opcional, por defecto: raíz del workspace o carpeta `docs/markdown/`)

---

## Reglas de conversión

### 1. Estructura y encabezados

- Los títulos del documento (Heading 1, 2, 3…) se convierten a `#`, `##`, `###`, etc.
- Si el PDF no tiene estilos explícitos, inferir jerarquía por tamaño/peso visual de fuente o posición.
- El título principal del documento (si existe) se convierte en `# Título`.

### 2. Texto y estilos

| Estilo original       | Equivalente Markdown         |
|-----------------------|------------------------------|
| Negrita               | `**texto**`                  |
| Cursiva               | `*texto*`                    |
| Negrita + cursiva     | `***texto***`                |
| Subrayado             | `<u>texto</u>` (HTML inline) |
| Tachado               | `~~texto~~`                  |
| Monoespaciado / código | `` `código` ``              |
| Superíndice           | `<sup>texto</sup>`           |
| Subíndice             | `<sub>texto</sub>`           |

### 3. Listas

- Listas con viñetas → listas Markdown con `-`
- Listas numeradas → listas Markdown con `1.`, `2.`, etc.
- Listas anidadas → indentación con 2 espacios por nivel

### 4. Tablas

- Convertir tablas a formato Markdown estándar con pipes `|`
- Si la tabla tiene encabezados, usar la línea separadora `|---|`
- Si la tabla es compleja (celdas combinadas), notar la limitación con un comentario HTML: `<!-- Tabla simplificada: celdas combinadas no soportadas en Markdown estándar -->`
- Preservar todo el contenido textual de celdas combinadas distribuyéndolo en celdas separadas

### 5. Links e hipervínculos

- Hipervínculos → `[texto del link](URL)`
- Si solo hay URL sin texto descriptivo → `<URL>`
- Referencias cruzadas internas (ej. "ver sección 3") → conservar el texto literal

### 6. Imágenes

- Si el archivo contiene imágenes incrustadas que no pueden extraerse:
  - Insertar marcador: `![Imagen: descripción o caption si existe](imagen_no_disponible)`
  - Añadir nota al pie: `> **Nota:** El documento original contiene imágenes que no pudieron extraerse automáticamente.`
- Si las imágenes tienen caption o texto alternativo, preservarlo en el alt text.

### 7. Bloques de código y texto preformateado

- Bloques de código (`Courier New`, `Consolas`, estilo `Code`) → bloques de código Markdown con triple backtick y lenguaje si es detectable:
  ````
  ```lenguaje
  código
  ```
  ````

### 8. Citas y notas al pie

- Citas en bloque → `> texto de la cita`
- Notas al pie → conservar el texto al final de la sección con formato:
  ```
  ---
  **Notas:**
  [^1]: Contenido de la nota al pie
  ```

### 9. Metadatos del documento

Si el archivo tiene metadatos (título, autor, fecha de creación, etc.), incluirlos al inicio del markdown en un bloque YAML:

```yaml
---
title: "Título del documento"
author: "Nombre del autor"
date: "YYYY-MM-DD"
source_file: "nombre_original.pdf"
---
```

### 10. Separadores y saltos de página

- Saltos de página → `---` (línea horizontal)
- Separadores de sección visibles → `---`

---

## Reglas de fidelidad

1. **No omitir texto**: todo el contenido textual del documento original debe aparecer en el Markdown.
2. **No inventar**: si un elemento no tiene equivalente directo en Markdown, usar HTML inline o una nota aclaratoria, pero nunca omitir el contenido.
3. **Orden preservado**: el contenido debe aparecer en el mismo orden que en el documento original.
4. **Encoding**: usar UTF-8. Preservar caracteres especiales, tildes, símbolos y caracteres no latinos.
5. **Espaciado**: respetar los saltos de línea significativos. No colapsar párrafos separados en uno solo.

---

## Output esperado

### Archivo Markdown generado

```markdown
---
title: "Título del documento"
author: "Autor (si disponible)"
date: "YYYY-MM-DD"
source_file: "nombre_original.ext"
converted_at: "YYYY-MM-DD HH:MM:SS"
---

# Título principal

## Sección 1

Texto del párrafo...

### Subsección 1.1

- Elemento de lista
- Otro elemento

| Columna 1 | Columna 2 |
|-----------|-----------|
| Valor     | Valor     |

...
```

### Resumen de conversión (al pie del archivo o en consola)

```
## Resumen de conversión

- **Archivo origen:** nombre_original.pdf
- **Archivo destino:** nombre_original_20260407_1200.md
- **Encabezados detectados:** X
- **Tablas convertidas:** X
- **Imágenes encontradas:** X (extraídas / no disponibles)
- **Notas al pie:** X
- **Advertencias:** [lista de limitaciones encontradas, si aplica]
```

---

## Reglas de generación del archivo Markdown

1. **Nombre del archivo:**
   - Un solo archivo: `[NombreOriginalSinExt]_[YYYYMMDD_HHmm].md` (sin espacios, sin tildes)
   - Múltiples archivos: un `.md` por cada archivo con la misma convención
2. **Ubicación:**
   - Si el usuario especifica carpeta destino → usar esa carpeta
   - Si no se especifica → guardar en `docs/markdown/` relativa al workspace. Crear la carpeta si no existe.
3. **Timestamp:** Incluir siempre en el bloque de metadatos YAML: `converted_at: "YYYY-MM-DD HH:MM:SS"`
4. Usar la herramienta `create_file` para escribir el archivo con el contenido convertido.

---

## Manejo de limitaciones

| Situación                              | Acción                                                                 |
|----------------------------------------|------------------------------------------------------------------------|
| PDF con texto escaneado (imagen/OCR)   | Advertir al usuario: el texto puede no ser extraíble con fidelidad     |
| PDF con protección de copia            | Informar que el archivo está protegido y no puede procesarse           |
| Tablas con celdas combinadas           | Simplificar y añadir comentario HTML indicando la limitación           |
| Fórmulas matemáticas                   | Convertir a LaTeX inline/block si es posible, o preservar como texto   |
| Imágenes sin caption                   | Usar marcador con descripción genérica: `![Imagen sin descripción]()`  |
| Columnas múltiples (layout tipo revista)| Convertir cada columna como sección secuencial con nota aclaratoria   |

---

## Notas generales

- Priorizar fidelidad del contenido sobre perfección del formato
- Si hay ambigüedad en la jerarquía de encabezados, optar por la estructura más conservadora
- Para documentos muy largos, procesar sección a sección para mantener precisión
- Indicar siempre al usuario si se detectaron elementos que no pudieron convertirse con fidelidad total
