# Skill: parafrasear

## Descripción
Parafraseador académico de párrafos en español. Traduce al inglés, parafraseea mediante back-translation (EN→DE→EN), traduce de vuelta al español y calcula el porcentaje de similitud con el texto original. Genera un informe Markdown con los resultados y una evaluación del nivel de parafraseo.

## Cuándo usar este skill
Usar cuando el usuario:
- Pida parafrasear un párrafo en español
- Quiera reducir similitud con un texto original (para evitar plagio)
- Necesite reescribir un fragmento académico manteniendo el significado
- Quiera ver cuánto cambió un texto después de parafrasearlo

## Método de parafraseo: Back-Translation
1. **ES → EN** (Google Translate)
2. **EN → DE** (alemán como idioma intermedio — produce reordenamiento sintáctico natural)
3. **DE → EN** (vuelta al inglés — el texto ya está parafraseado)
4. **EN → ES** (resultado final en español)

Este método no requiere API keys ni modelos de IA. Usa Google Translate de forma gratuita.

## Umbrales de similitud

| Similitud | Estado | Interpretación |
|-----------|--------|----------------|
| ≥ 75% | 🔴 ALTA | El texto cambió poco. Riesgo de detección por Turnitin |
| 40–74% | 🟡 MODERADA | Parafraseo aceptable. Revisar manualmente |
| < 40% | ✅ BAJA | Buen parafraseo. Bajo riesgo de detección |

La similitud se calcula en dos dimensiones:
- **Similitud de caracteres**: SequenceMatcher a nivel de texto completo
- **Similitud de palabras clave**: palabras en común (sin stopwords) / total palabras únicas del original

El porcentaje final es el **promedio ponderado** (60% palabra clave + 40% caracteres).

## Archivos del skill

```
.github/skills/parafrasear/
├── SKILL.md           ← este archivo
└── parafrasear.py     ← script ejecutable
```

## Dependencias

```bash
pip install deep-translator
```

No requiere API keys.

## Uso

```bash
# Párrafo directo como argumento
python parafrasear.py --texto "La gestión del talento humano es fundamental para el éxito organizacional."

# Desde archivo .txt
python parafrasear.py --file parrafo.txt

# Cambiar idioma intermedio (default: de = alemán)
python parafrasear.py --texto "..." --via fr

# Guardar resultado en carpeta personalizada
python parafrasear.py --texto "..." --out resultados/

# Múltiples párrafos desde archivo (uno por línea)
python parafrasear.py --file parrafos.txt --multi
```

## Salida

Archivo: `parafraseos/PARA-<fecha>-<hora>.md`

Incluye:
- Texto original
- Traducción al inglés
- Paráfrasis en inglés
- Resultado en español
- Similitud (porcentaje + semáforo)
- Historial de versiones (si se usa `--multi`)

## Idiomas intermedios disponibles

| Código | Idioma | Efecto típico |
|--------|--------|---------------|
| `de` | Alemán | Reordenamiento fuerte (recomendado) |
| `fr` | Francés | Cambios léxicos moderados |
| `pt` | Portugués | Cambios mínimos (similar al español) |
| `ja` | Japonés | Cambios muy fuertes (puede perder matiz) |
| `zh-CN` | Chino | Cambios muy fuertes |

## Integración con verificar-referencias
Úsalo junto a `verificar-referencias` para verificar que las fuentes citadas en el texto original también estén referenciadas en el texto parafraseado.
