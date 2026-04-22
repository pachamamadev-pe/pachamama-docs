"""
parafrasear.py
Parafraseador académico con DOS opciones simultáneas por párrafo:

  Opción A — IA:      ES → EN → Pegasus Paraphrase (modelo IA) → EN → ES
  Opción B — Pivot:   ES → EN → [idioma distante] → EN → ES

Dependencias:
    pip install deep-translator transformers torch sentencepiece

Uso:
    python parafrasear.py --texto "La gestión del talento humano es clave."
    python parafrasear.py --file parrafo.txt
    python parafrasear.py --file parrafos.txt --multi
    python parafrasear.py --texto "..." --via zh-CN   # cambiar idioma pivote de Opción B
"""

import argparse
import os
import re
import sys
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("ERROR: Instala deep-translator con:  pip install deep-translator")
    sys.exit(1)

# ─── Modelo Pegasus (carga lazy, solo una vez por sesión) ────────────────────
_pegasus_model     = None
_pegasus_tokenizer = None

def _load_pegasus():
    global _pegasus_model, _pegasus_tokenizer
    if _pegasus_model is None:
        try:
            from transformers import PegasusForConditionalGeneration, PegasusTokenizer
            print("  [IA] Cargando modelo Pegasus Paraphrase (primera vez: ~500 MB)...")
            model_name = "tuner007/pegasus_paraphrase"
            _pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
            _pegasus_model     = PegasusForConditionalGeneration.from_pretrained(model_name)
            print("  [IA] Modelo listo.")
        except ImportError:
            print("ERROR: Instala transformers y torch:  pip install transformers torch sentencepiece")
            sys.exit(1)
    return _pegasus_model, _pegasus_tokenizer


def _extraer_anclas(text_en: str) -> list[str]:
    """
    Extrae términos clave que NO deben perderse en la paráfrasis:
    - Secuencias de palabras capitalizadas (nombres propios, ubicaciones)
    - Números (incluyendo ordinales, años, porcentajes)
    - Acrónimos (2+ letras mayúsculas)
    Retorna lista ordenada de mayor a menor longitud.
    """
    anclas = []

    # Secuencias de palabras capitalizadas (≥2 palabras): e.g. "Villa El Salvador"
    for m in re.finditer(r"\b([A-Z][a-zA-Z]+(?:\s+(?:of|the|de|del|la|el|and|for|in|at|by)?\s*[A-Z][a-zA-Z]+)+)\b", text_en):
        anclas.append(m.group(1))

    # Palabras capitalizadas simples que NO son la primera de la oración
    # (indicadas por no ir después de un punto/inicio de cadena)
    for m in re.finditer(r"(?<=[a-záéíóú,;:\s])([A-Z][a-z]{2,})\b", text_en):
        w = m.group(1)
        # ignorar palabras genéricas en inglés que suelen capitalizarse
        _genericas = {"The","A","An","In","Of","For","And","Or","To","At",
                      "By","On","With","From","This","That","These","Those"}
        if w not in _genericas:
            anclas.append(w)

    # Números y porcentajes
    for m in re.finditer(r"\b\d+[.,]?\d*\s*%?\b", text_en):
        anclas.append(m.group(0).strip())

    # Acrónimos: 2+ letras mayúsculas seguidas
    for m in re.finditer(r"\b[A-Z]{2,}\b", text_en):
        anclas.append(m.group(0))

    # Deduplicar preservando orden; ordenar de mayor a menor longitud
    seen = set()
    result = []
    for a in anclas:
        a = a.strip()
        if a and a not in seen:
            seen.add(a)
            result.append(a)
    result.sort(key=len, reverse=True)
    return result


def _cobertura_anclas(anclas: list[str], texto: str) -> float:
    """
    Porcentaje de anclas que aparecen en el texto (case-insensitive).
    """
    if not anclas:
        return 1.0
    texto_low = texto.lower()
    found = sum(1 for a in anclas if a.lower() in texto_low)
    return found / len(anclas)


def parafrasear_pegasus_en(text_en: str, anclas: list[str] | None = None) -> tuple[str, list[str]]:
    """
    Parafrasea un texto en inglés usando Pegasus.
    Genera NUM_BEAMS candidatos y elige el que mejor preserva las anclas.
    Retorna (mejor_parafrasis, anclas_perdidas).
    """
    if anclas is None:
        anclas = _extraer_anclas(text_en)

    model, tokenizer = _load_pegasus()
    NUM_BEAMS = 10
    NUM_SEQS  = min(5, NUM_BEAMS)
    max_out   = min(len(text_en.split()) * 2 + 30, 256)

    inputs = tokenizer(
        [text_en],
        truncation=True,
        padding="longest",
        max_length=512,
        return_tensors="pt",
    )
    result = model.generate(
        **inputs,
        max_length=max_out,
        num_beams=NUM_BEAMS,
        num_return_sequences=NUM_SEQS,
        early_stopping=True,
    )
    candidates = tokenizer.batch_decode(result, skip_special_tokens=True)

    # Elegir el candidato con mayor cobertura de anclas
    best     = candidates[0]
    best_cov = _cobertura_anclas(anclas, best)
    for c in candidates[1:]:
        cov = _cobertura_anclas(anclas, c)
        if cov > best_cov:
            best_cov = cov
            best = c

    anclas_perdidas = [a for a in anclas if a.lower() not in best.lower()]
    return best, anclas_perdidas

# ─── Configuración ─────────────────────────────────────────────────────────

# Umbral de similitud (porcentaje)
UMBRAL_ALTA      = 75   # >= ALTA: cambio insuficiente (riesgo Turnitin)
UMBRAL_MODERADA  = 40   # >= MODERADA: aceptable
                        # <  MODERADA: bien parafraseado

# Stopwords básicas en español para el cálculo de similitud por palabras clave
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","por","un","con","una",
    "su","para","es","al","lo","como","más","o","pero","sus","le","ya","ha",
    "me","si","sin","sobre","este","entre","cuando","ser","son","dos","también",
    "fue","hay","era","muy","bien","uno","porque","todo","esta","han","puede",
    "que","le","así","hasta","desde","nos","durante","ni","contra","ese","que",
    "esto","cual","donde","quien","aunque","tanto","mientras","cada","estos",
    "ante","incluso","tras","esto","mismo","aquí","aún","luego","después",
}

# ─── Traducción ─────────────────────────────────────────────────────────────

def translate(text: str, source: str, target: str) -> str:
    """Traduce un texto usando Google Translate via deep-translator."""
    try:
        translated = GoogleTranslator(source=source, target=target).translate(text)
        return translated or text
    except Exception as e:
        print(f"  AVISO traducción ({source}→{target}): {e}")
        return text


def parafrasear_opcion_a(texto_es: str) -> dict:
    """
    Opción A — IA:
    ES → EN → Pegasus paraphrase (inglés, anchor-aware) → EN → ES
    """
    en_original  = translate(texto_es, source="es", target="en")
    anclas       = _extraer_anclas(en_original)

    en_parafraseado, anclas_perdidas = parafrasear_pegasus_en(en_original, anclas)
    es_resultado = translate(en_parafraseado, source="en", target="es")

    return {
        "tipo":             "A",
        "label":            "Paráfrasis por IA (Pegasus)",
        "original_es":      texto_es,
        "paso1_en":         en_original,
        "paso2_via":        en_parafraseado,
        "via_lang":         "ia",
        "paso3_en_para":    en_parafraseado,
        "resultado_es":     es_resultado,
        "anclas":           anclas,
        "anclas_perdidas":  anclas_perdidas,
    }


def parafrasear_opcion_b(texto_es: str, via: str = "ja") -> dict:
    """
    Opción B — Pivot distante:
    ES → EN → [idioma distante] → EN → ES
    """
    en_original     = translate(texto_es, source="es", target="en")
    via_text        = translate(en_original, source="en", target=via)
    en_parafraseado = translate(via_text,    source=via,  target="en")
    es_resultado    = translate(en_parafraseado, source="en", target="es")

    return {
        "tipo":          "B",
        "label":         f"Back-translation [{VIA_NOMBRES.get(via, via.upper())}]",
        "original_es":   texto_es,
        "paso1_en":      en_original,
        "paso2_via":     via_text,
        "via_lang":      via,
        "paso3_en_para": en_parafraseado,
        "resultado_es":  es_resultado,
    }


# ─── Cálculo de similitud ───────────────────────────────────────────────────

def _normalizar(texto: str) -> str:
    """Normaliza el texto: minúsculas, sin puntuación extra."""
    texto = texto.lower()
    texto = re.sub(r"[^\w\sáéíóúüàèìòùâêîôûñç]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def similitud_caracteres(a: str, b: str) -> float:
    """Similitud a nivel de caracteres (SequenceMatcher)."""
    a = _normalizar(a)
    b = _normalizar(b)
    return SequenceMatcher(None, a, b).ratio() * 100


def similitud_palabras_clave(original: str, parafraseado: str) -> float:
    """
    Jaccard de palabras clave (sin stopwords).
    Mide cuántas palabras significativas coinciden.
    """
    def palabras_clave(texto: str) -> set:
        tokens = set(_normalizar(texto).split())
        return tokens - STOPWORDS_ES

    orig_kw = palabras_clave(original)
    para_kw = palabras_clave(parafraseado)

    if not orig_kw:
        return 0.0

    interseccion = orig_kw & para_kw
    union = orig_kw | para_kw
    return (len(interseccion) / len(union)) * 100 if union else 0.0


def calcular_similitud(original_es: str, resultado_es: str) -> dict:
    """
    Calcula la similitud combinada entre el párrafo original y el parafraseado.
    Retorna: {chars_pct, keywords_pct, combined_pct, nivel, palabras_en_comun}
    """
    chars_pct    = round(similitud_caracteres(original_es, resultado_es), 1)
    keywords_pct = round(similitud_palabras_clave(original_es, resultado_es), 1)

    # Promedio ponderado: 60% palabras clave, 40% caracteres
    combined_pct = round(keywords_pct * 0.60 + chars_pct * 0.40, 1)

    if combined_pct >= UMBRAL_ALTA:
        nivel = "ALTA"
        icon  = "🔴"
    elif combined_pct >= UMBRAL_MODERADA:
        nivel = "MODERADA"
        icon  = "🟡"
    else:
        nivel = "BAJA"
        icon  = "✅"

    # Palabras en común (sin stopwords)
    def kw(t):
        return set(_normalizar(t).split()) - STOPWORDS_ES
    en_comun = sorted(kw(original_es) & kw(resultado_es))

    return {
        "chars_pct":    chars_pct,
        "keywords_pct": keywords_pct,
        "combined_pct": combined_pct,
        "nivel":        nivel,
        "icon":         icon,
        "en_comun":     en_comun,
    }


# ─── Generación del informe Markdown ────────────────────────────────────────

VIA_NOMBRES = {
    "ia":    "IA (Pegasus)",
    "de":    "Alemán",
    "fr":    "Francés",
    "pt":    "Portugués",
    "it":    "Italiano",
    "ja":    "Japonés",
    "zh-CN": "Chino (Simp.)",
    "ru":    "Ruso",
    "ar":    "Árabe",
    "nl":    "Neerlandés",
}

def _sim_bloque(sim: dict, original_es: str, resultado_es: str) -> list[str]:
    """Genera las líneas Markdown del análisis de similitud."""
    lines = []
    lines.append("#### Análisis de similitud\n")
    lines.append("| Métrica | Valor |")
    lines.append("|---------|-------|")
    lines.append(f"| Similitud de caracteres | {sim['chars_pct']}% |")
    lines.append(f"| Similitud de palabras clave | {sim['keywords_pct']}% |")
    lines.append(f"| **Similitud combinada** | **{sim['combined_pct']}%** |")
    lines.append(f"| Nivel | {sim['icon']} **{sim['nivel']}** |")
    lines.append("")

    bar_filled = round(sim["combined_pct"] / 5)
    bar_empty  = 20 - bar_filled
    bar = "█" * bar_filled + "░" * bar_empty
    lines.append(f"```\nSimilitud: [{bar}] {sim['combined_pct']}%\n```\n")

    if sim["nivel"] == "ALTA":
        interp = (
            f"🔴 **Similitud alta ({sim['combined_pct']}%).** "
            "El texto conserva demasiado del original. "
            "Turnitin podría detectarlo. "
            "Considera reescribir manualmente o usar la Opción B con `--via ar`."
        )
    elif sim["nivel"] == "MODERADA":
        interp = (
            f"🟡 **Similitud moderada ({sim['combined_pct']}%).** "
            "Parafraseo aceptable. Revisar que el significado esté preservado."
        )
    else:
        interp = (
            f"✅ **Similitud baja ({sim['combined_pct']}%).** "
            "Buen parafraseo. Verificar que el sentido académico se conserva."
        )
    lines.append(f"{interp}\n")

    if sim["en_comun"]:
        comun_str = ", ".join(f"`{p}`" for p in sim["en_comun"][:12])
        if len(sim["en_comun"]) > 12:
            comun_str += f" _(y {len(sim['en_comun']) - 12} más)_"
        lines.append(f"**Palabras clave en común:** {comun_str}\n")

    return lines


def build_report(resultado_a: dict, sim_a: dict,
                 resultado_b: dict, sim_b: dict,
                 idx: int = 1, total: int = 1) -> str:
    """Genera el bloque Markdown con las DOS opciones de paráfrasis."""
    timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M")
    via_nombre = VIA_NOMBRES.get(resultado_b["via_lang"], resultado_b["via_lang"].upper())

    lines = []

    if total > 1:
        lines.append(f"## Párrafo {idx} de {total}\n")

    # ── Texto original
    lines.append("### Texto original\n")
    lines.append(f"> {resultado_a['original_es']}\n")

    # ──────────────────────────────────────────────────────────
    lines.append("---")
    lines.append("## Opción A — Paráfrasis por IA (Pegasus)\n")
    lines.append("*Pipeline: ES → EN → Pegasus Paraphrase (anchor-aware) → EN → ES*\n")

    lines.append("#### Proceso\n")
    lines.append("| Paso | Descripción | Texto |")
    lines.append("|------|-------------|-------|")
    lines.append(f"| 1 | Español → Inglés | {resultado_a['paso1_en']} |")
    lines.append(f"| 2 | Paráfrasis IA (inglés) | {resultado_a['paso3_en_para']} |")
    lines.append(f"| 3 | Inglés → Español | {resultado_a['resultado_es']} |")
    lines.append("")

    # Cobertura de anclas
    anclas         = resultado_a.get("anclas", [])
    anclas_perdidas = resultado_a.get("anclas_perdidas", [])
    if anclas:
        n_ok  = len(anclas) - len(anclas_perdidas)
        pct_ok = round(n_ok / len(anclas) * 100)
        icon_cov = "✅" if not anclas_perdidas else ("⚠️" if pct_ok >= 70 else "🔴")
        lines.append("#### Cobertura de información clave\n")
        lines.append(f"| Términos detectados | Preservados | Perdidos | Cobertura |")
        lines.append(f"|---------------------|-------------|----------|-----------|")
        lines.append(f"| {len(anclas)} | {n_ok} | {len(anclas_perdidas)} | {icon_cov} {pct_ok}% |")
        lines.append("")
        if anclas_perdidas:
            perdidos_str = ", ".join(f"`{a}`" for a in anclas_perdidas)
            lines.append(f"> ⚠️ **Información que puede haberse perdido:** {perdidos_str}  ")
            lines.append(f"> Verificar manualmente que el resultado en español incluye estos términos.\n")
        elif anclas:
            ok_str = ", ".join(f"`{a}`" for a in anclas[:8])
            lines.append(f"> ✅ Todos los términos clave preservados: {ok_str}\n")

    lines.append("#### Resultado\n")
    lines.append(f"> **{resultado_a['resultado_es']}**\n")

    lines += _sim_bloque(sim_a, resultado_a["original_es"], resultado_a["resultado_es"])

    # ──────────────────────────────────────────────────────────
    lines.append("---")
    lines.append(f"## Opción B — Back-translation [{via_nombre}]\n")
    lines.append(f"*Pipeline: ES → EN → {via_nombre} → EN → ES*\n")

    lines.append("#### Proceso\n")
    lines.append("| Paso | Idioma | Texto |")
    lines.append("|------|--------|-------|")
    lines.append(f"| 1 | Español → Inglés | {resultado_b['paso1_en']} |")
    lines.append(f"| 2 | Inglés → {via_nombre} | {resultado_b['paso2_via']} |")
    lines.append(f"| 3 | {via_nombre} → Inglés | {resultado_b['paso3_en_para']} |")
    lines.append(f"| 4 | Inglés → Español | {resultado_b['resultado_es']} |")
    lines.append("")

    lines.append("#### Resultado\n")
    lines.append(f"> **{resultado_b['resultado_es']}**\n")

    lines += _sim_bloque(sim_b, resultado_b["original_es"], resultado_b["resultado_es"])

    # ── Comparativa final
    lines.append("---")
    lines.append("## Comparativa\n")
    lines.append("| | Opción A (IA) | Opción B (Pivot) |")
    lines.append("|---|---|---|")
    lines.append(f"| Similitud combinada | {sim_a['combined_pct']}% {sim_a['icon']} | {sim_b['combined_pct']}% {sim_b['icon']} |")
    lines.append(f"| Palabras clave en común | {len(sim_a['en_comun'])} | {len(sim_b['en_comun'])} |")

    # Recomendación
    mejor = "A (IA)" if sim_a["combined_pct"] <= sim_b["combined_pct"] else f"B ({via_nombre})"
    lines.append("")
    lines.append(f"**Recomendación:** Usar Opción **{mejor}** (menor similitud con el original).\n")

    lines.append("---")
    lines.append(f"*Generado: {timestamp} · Opciones: IA + pivot {via_nombre} · transformers + deep-translator*")

    return "\n".join(lines)


def build_multi_report(items: list[dict], via: str) -> str:
    """Genera el informe completo para múltiples párrafos (2 opciones c/u)."""
    timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M")
    via_nombre = VIA_NOMBRES.get(via, via.upper())
    total      = len(items)

    avg_a = round(sum(it["sim_a"]["combined_pct"] for it in items) / total, 1) if total else 0
    avg_b = round(sum(it["sim_b"]["combined_pct"] for it in items) / total, 1) if total else 0

    header = [
        "# Parafraseo de Párrafos — Doble Opción\n",
        f"**Fecha:** {timestamp}  ",
        f"**Idioma pivot (Opción B):** {via_nombre}  ",
        f"**Total de párrafos:** {total}\n",
        "| Métrica | Opción A (IA) | Opción B (Pivot) |",
        "|---------|--------------|-----------------|",
        f"| Similitud promedio | {avg_a}% | {avg_b}% |",
        "",
        "---\n",
    ]

    blocks = []
    for i, it in enumerate(items, 1):
        blocks.append(build_report(
            it["resultado_a"], it["sim_a"],
            it["resultado_b"], it["sim_b"],
            idx=i, total=total,
        ))

    return "\n".join(header) + "\n".join(blocks)


# ─── Punto de entrada ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Parafraseador con 2 opciones: IA (Pegasus) + pivot distante"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--texto", "-t", help="Párrafo en español a parafrasear")
    group.add_argument("--file",  "-f", help="Archivo .txt con el párrafo (o párrafos con --multi)")

    parser.add_argument("--via", default="ja",
                        help="Idioma pivot para Opción B (default: ja = japonés). "
                             "Opciones: ja, zh-CN, ar, ru, fr, pt, it, nl")
    parser.add_argument("--multi", action="store_true",
                        help="Procesa cada línea no vacía como un párrafo independiente")
    parser.add_argument("--out", default="parafraseos",
                        help="Carpeta de salida (default: parafraseos/)")
    args = parser.parse_args()

    # Reunir párrafos
    if args.texto:
        parrafos = [args.texto.strip()]
    else:
        if not os.path.exists(args.file):
            print(f"ERROR: No se encuentra el archivo: {args.file}")
            sys.exit(1)
        contenido = Path(args.file).read_text(encoding="utf-8", errors="ignore")
        if args.multi:
            parrafos = [p.strip() for p in contenido.splitlines() if p.strip()]
        else:
            parrafos = [contenido.strip()]

    parrafos = [p for p in parrafos if len(p) > 10]
    if not parrafos:
        print("ERROR: No se encontraron párrafos válidos.")
        sys.exit(1)

    via_nombre = VIA_NOMBRES.get(args.via, args.via.upper())
    print(f"\n{'='*60}")
    print(f"  Parafraseador — DOS opciones por párrafo")
    print(f"  Opción A: IA (Pegasus Paraphrase)")
    print(f"  Opción B: Pivot [{via_nombre}]")
    print(f"  Párrafos: {len(parrafos)}")
    print(f"{'='*60}\n")

    items = []
    for i, parrafo in enumerate(parrafos, 1):
        preview = parrafo[:65] + "..." if len(parrafo) > 65 else parrafo
        print(f"[{i}/{len(parrafos)}] {preview}")

        print(f"  → Opción A (IA)...")
        resultado_a = parafrasear_opcion_a(parrafo)
        sim_a = calcular_similitud(resultado_a["original_es"], resultado_a["resultado_es"])
        print(f"     {sim_a['icon']} {sim_a['nivel']} ({sim_a['combined_pct']}%)")

        print(f"  → Opción B ({via_nombre})...")
        resultado_b = parafrasear_opcion_b(parrafo, via=args.via)
        sim_b = calcular_similitud(resultado_b["original_es"], resultado_b["resultado_es"])
        print(f"     {sim_b['icon']} {sim_b['nivel']} ({sim_b['combined_pct']}%)\n")

        items.append({
            "resultado_a": resultado_a, "sim_a": sim_a,
            "resultado_b": resultado_b, "sim_b": sim_b,
        })

    # Generar informe
    os.makedirs(args.out, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(args.out, f"PARA-{timestamp_str}.md")

    if len(items) == 1:
        report = "# Parafraseo de Párrafo — Doble Opción\n\n" + build_report(
            items[0]["resultado_a"], items[0]["sim_a"],
            items[0]["resultado_b"], items[0]["sim_b"],
        )
    else:
        report = build_multi_report(items, via=args.via)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    # Resumen en consola
    print(f"{'='*60}")
    print(f"  RESUMEN")
    print(f"{'─'*60}")
    print(f"  {'#':<4} {'Opción A (IA)':<22} {'Opción B (Pivot)':<22}")
    print(f"  {'─'*46}")
    for i, it in enumerate(items[:8], 1):
        a = it["sim_a"]
        b = it["sim_b"]
        print(f"  {i:<4} {a['icon']} {a['combined_pct']:>5}% {a['nivel']:<12}  "
              f"{b['icon']} {b['combined_pct']:>5}% {b['nivel']}")
    if len(items) > 8:
        print(f"  ... ({len(items) - 8} más)")
    print(f"{'='*60}")
    print(f"\n  Informe guardado en: {out_path}\n")

    # Vista rápida en consola para un solo párrafo
    if len(items) == 1:
        r_a = items[0]["resultado_a"]
        r_b = items[0]["resultado_b"]
        print("─" * 60)
        print("  ORIGINAL:")
        print(f"  {r_a['original_es']}")
        print("─" * 60)
        print("  OPCIÓN A (IA):")
        print(f"  {r_a['resultado_es']}")
        print("─" * 60)
        print(f"  OPCIÓN B ({via_nombre}):")
        print(f"  {r_b['resultado_es']}")
        print("─" * 60 + "\n")


if __name__ == "__main__":
    main()
