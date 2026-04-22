"""
verificar_referencias.py
Verifica autenticidad de referencias bibliográficas contra CrossRef, OpenAlex y Semantic Scholar.
APIs utilizadas: gratuitas, sin API key requerida.

Uso:
    python verificar_referencias.py --file tesis.docx
    python verificar_referencias.py --file refs.txt --email tu@email.com
    python verificar_referencias.py --file paper.pdf --section "Bibliografía" --out resultados/    python verificar_referencias.py --file informe_turnitin.pdf --turnitin"""

import argparse
import re
import time
import json
import os
import sys
from datetime import date
from difflib import SequenceMatcher
from urllib.parse import quote_plus
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: Instala requests con:  pip install requests")
    sys.exit(1)

# ─── Configuración ─────────────────────────────────────────────────────────

DEFAULT_EMAIL = "verificador@academico.pe"
PAUSE_BETWEEN_CALLS = 0.6   # segundos (CrossRef polite pool)
MIN_SCORE_VERIFIED = 85     # % para VERIFICADA
MIN_SCORE_POSSIBLE = 55     # % para POSIBLE

# ─── Extracción de texto ────────────────────────────────────────────────────

def extract_text_docx(path: str) -> str:
    try:
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except ImportError:
        print("ERROR: Instala python-docx con:  pip install python-docx")
        sys.exit(1)


def extract_text_pdf(path: str) -> str:
    try:
        import fitz  # pymupdf
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except ImportError:
        pass
    try:
        from pdfminer.high_level import extract_text as pdfminer_extract
        return pdfminer_extract(path)
    except ImportError:
        print("ERROR: Instala pymupdf o pdfminer.six con:")
        print("  pip install pymupdf   (recomendado)")
        print("  pip install pdfminer.six  (alternativa)")
        sys.exit(1)


def extract_text(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".docx":
        return extract_text_docx(path)
    elif ext == ".pdf":
        return extract_text_pdf(path)
    elif ext in (".txt", ".md"):
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    else:
        print(f"AVISO: Extensión {ext} no reconocida. Intentando como texto plano.")
        return Path(path).read_text(encoding="utf-8", errors="ignore")


# ─── Detección de sección de referencias ───────────────────────────────────

SECTION_KEYWORDS = [
    r"referencias\s*bibliogr[aá]ficas",
    r"bibliograf[ií]a",
    r"references",
    r"bibliography",
    r"fuentes\s*consultadas",
    r"obras\s*citadas",
    r"literatura\s*citada",
    r"citas\s*bibliogr[aá]ficas",
]

def find_references_section(full_text: str, section_hint: str = None) -> str:
    """Encuentra y retorna solo el bloque de referencias del texto completo."""
    lines = full_text.split("\n")
    start_idx = None

    patterns = [re.compile(section_hint, re.IGNORECASE)] if section_hint else \
               [re.compile(p, re.IGNORECASE) for p in SECTION_KEYWORDS]

    for i, line in enumerate(lines):
        for pat in patterns:
            if pat.search(line.strip()) and len(line.strip()) < 80:
                start_idx = i + 1
                break
        if start_idx:
            break

    if start_idx is None:
        # No se encontró sección: devolver todo el texto
        print("AVISO: No se encontró sección de referencias. Procesando texto completo.")
        return full_text

    # Tomar hasta la siguiente sección de nivel similar o fin de documento
    block_lines = []
    next_section = re.compile(
        r"^\s*(\d+[\.\)]\s+)?[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{3,}$"
    )
    for line in lines[start_idx:]:
        if next_section.match(line) and len(block_lines) > 5:
            break
        block_lines.append(line)

    return "\n".join(block_lines)


# ─── Parseo de referencias individuales ────────────────────────────────────

# Patrones para detectar inicio de una nueva referencia
REF_START_PATTERNS = [
    re.compile(r"^\[\d+\]"),                         # [1] Vancouver/IEEE
    re.compile(r"^\d+\.\s+[A-ZÁÉÍÓÚÑ]"),             # 1. Apellido
    re.compile(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+,\s+[A-Z]"), # Apellido, A.
    re.compile(r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ]"),  # Apellido Nombre
]

def split_references(section_text: str) -> list[str]:
    """Divide el bloque de referencias en una lista de referencias individuales."""
    lines = [l.strip() for l in section_text.split("\n") if l.strip()]
    refs = []
    current = []

    for line in lines:
        is_new_ref = any(pat.match(line) for pat in REF_START_PATTERNS)
        if is_new_ref and current:
            refs.append(" ".join(current))
            current = [line]
        elif line:
            current.append(line)

    if current:
        refs.append(" ".join(current))

    # Filtrar líneas muy cortas (< 30 chars) que no son referencias
    refs = [r for r in refs if len(r) > 30]
    return refs


# ─── Parseo estructurado de una referencia ─────────────────────────────────

DOI_PATTERN = re.compile(r"10\.\d{4,9}/[^\s,]+")
YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")
TITLE_APA_PATTERN = re.compile(
    r"\(\d{4}[a-z]?\)\.\s+(.+?)\.\s+[*_]?[A-ZÁÉÍÓÚÑA-Z]", re.DOTALL
)
TITLE_GENERIC_PATTERN = re.compile(
    r'[\u201c"](.+?)[\u201d"]'  # Título entre comillas (rectas y tipográficas)
)

def parse_reference(ref_text: str) -> dict:
    """Extrae metadatos básicos de una referencia en texto libre."""
    result = {"raw": ref_text, "doi": None, "year": None, "title": None, "authors": []}

    # DOI
    doi_match = DOI_PATTERN.search(ref_text)
    if doi_match:
        result["doi"] = doi_match.group(0).rstrip(".,;)")

    # Año
    years = YEAR_PATTERN.findall(ref_text)
    if years:
        result["year"] = int(years[0])

    # Título (entre comillas — estilo IEEE/Vancouver)
    title_match = TITLE_GENERIC_PATTERN.search(ref_text)
    if title_match:
        result["title"] = title_match.group(1).strip()
    else:
        # APA: después de (año).
        apa_match = TITLE_APA_PATTERN.search(ref_text)
        if apa_match:
            result["title"] = apa_match.group(1).strip(". ")
        else:
            # Fallback: heurística — tomar fragmento central
            clean = re.sub(r"^\[\d+\]\s*", "", ref_text)          # quitar [n]
            clean = re.sub(r"^[\d]+\.\s*", "", clean)              # quitar "1."
            clean = re.sub(r"\b(19|20)\d{2}\b.*", "", clean)       # cortar en año
            parts = clean.split(".")
            # El título suele ser el fragmento de 3–15 palabras más largo
            candidates = [p.strip() for p in parts if 3 < len(p.split()) < 25]
            if candidates:
                result["title"] = max(candidates, key=len)

    return result


# ─── Extracción de fuentes de informe Turnitin ────────────────────────────────

# Etiquetas de tipo de fuente usadas por Turnitin (en varios idiomas)
TURNITIN_SOURCE_TYPES = re.compile(
    r"(internet\s+source[s]?|internet|publicacion|publication[s]?|"
    r"student\s+paper[s]?|submitted\s+work|fuente\s+de\s+internet|"
    r"trabajo\s+de\s+alumno|publicaci[oó]n)",
    re.IGNORECASE
)
TURNITIN_PERCENT = re.compile(r"(\d{1,3})\s*%")
TURNITIN_URL = re.compile(r"https?://[^\s<>\"]+|www\.[^\s<>\"]+")
TURNITIN_ENTRY_NUM = re.compile(r"^\s*(\d{1,3})\s*$")


def extract_turnitin_sources(text: str) -> list[dict]:
    """
    Extrae la lista de fuentes del informe de similitud Turnitin (PDF extraído a texto).
    Retorna lista de dicts con: number, title, url, source_type, similarity_pct, raw.
    """
    lines = text.split("\n")

    # 1. Intentar localizar la sección de fuentes
    source_section_pat = re.compile(
        r"(sources?|fuentes|source\s+list|lista\s+de\s+fuentes|"
        r"submitted\s+to|internet\s+sources?|"  
        r"similarity\s+by\s+source|coincidencias\s+por\s+fuente)",
        re.IGNORECASE
    )
    start_idx = 0
    for i, line in enumerate(lines):
        if source_section_pat.search(line) and len(line.strip()) < 60:
            start_idx = i
            break

    work_lines = lines[start_idx:]

    # 2. Construir bloques agrupados por número de entrada
    sources = []
    current_block = []
    current_num = None

    for line in work_lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Detectar nueva entrada numerada: "1" solo o "1." o "1 " al inicio
        num_only = TURNITIN_ENTRY_NUM.match(stripped)
        num_dot = re.match(r"^(\d{1,3})[.)]", stripped)
        num_inline = re.match(r"^(\d{1,3})\s+(.+)", stripped)

        if num_only:
            if current_block and current_num is not None:
                sources.append(_parse_turnitin_block(current_num, current_block))
            current_num = int(num_only.group(1))
            current_block = []
        elif num_dot and not num_inline:
            if current_block and current_num is not None:
                sources.append(_parse_turnitin_block(current_num, current_block))
            current_num = int(num_dot.group(1))
            rest = stripped[num_dot.end():].strip()
            current_block = [rest] if rest else []
        elif num_inline and int(num_inline.group(1)) <= 500:
            candidate_num = int(num_inline.group(1))
            # Solo tratar como nueva entrada si el número es consecutivo o mayor
            if current_num is None or candidate_num == (current_num + 1) or candidate_num == 1:
                if current_block and current_num is not None:
                    sources.append(_parse_turnitin_block(current_num, current_block))
                current_num = candidate_num
                current_block = [num_inline.group(2).strip()]
            else:
                current_block.append(stripped)
        else:
            if current_num is not None:
                current_block.append(stripped)

    if current_block and current_num is not None:
        sources.append(_parse_turnitin_block(current_num, current_block))

    # Si no detectamos estructura numerada, fallback: buscar líneas con URL + porcentaje
    if len(sources) < 3:
        sources = _fallback_turnitin_parse(text)

    return sources


def _parse_turnitin_block(num: int, block_lines: list[str]) -> dict:
    """Convierte un bloque de líneas de una fuente Turnitin en un dict estructurado."""
    raw = " | ".join(block_lines)
    entry = {
        "number": num,
        "raw": raw,
        "title": None,
        "url": None,
        "doi": None,
        "source_type": None,
        "similarity_pct": None,
        "year": None,
    }

    # Extraer porcentaje de similitud
    for line in block_lines:
        pct_match = TURNITIN_PERCENT.search(line)
        if pct_match:
            entry["similarity_pct"] = int(pct_match.group(1))
            break

    # Extraer URL
    for line in block_lines:
        url_match = TURNITIN_URL.search(line)
        if url_match:
            entry["url"] = url_match.group(0).rstrip(".,;)")
            break

    # Extraer DOI desde URL o texto
    doi_match = DOI_PATTERN.search(raw)
    if doi_match:
        entry["doi"] = doi_match.group(0).rstrip(".,;)")
    elif entry["url"] and "doi.org/" in entry["url"]:
        entry["doi"] = re.sub(r".*doi\.org/", "", entry["url"]).rstrip(".,;)")

    # Extraer tipo de fuente
    type_match = TURNITIN_SOURCE_TYPES.search(raw)
    if type_match:
        entry["source_type"] = type_match.group(0).strip()

    # Extraer título: primera línea que no sea URL, porcentaje ni tipo de fuente
    for line in block_lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        if TURNITIN_URL.match(line_clean):
            continue
        if TURNITIN_PERCENT.fullmatch(line_clean):
            continue
        if TURNITIN_SOURCE_TYPES.fullmatch(line_clean):
            continue
        if re.fullmatch(r"\d{1,3}\s*%?", line_clean):
            continue
        # Ignorar líneas muy cortas o que solo son números
        if len(line_clean) < 5:
            continue
        entry["title"] = line_clean[:300]
        break

    # Año
    year_match = YEAR_PATTERN.search(raw)
    if year_match:
        entry["year"] = int(year_match.group(0))

    return entry


def _fallback_turnitin_parse(text: str) -> list[dict]:
    """Parseo heurístico alternativo: busca pares URL + porcentaje en el texto completo."""
    sources = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        pct = TURNITIN_PERCENT.search(line)
        url = TURNITIN_URL.search(line)
        if pct and url:
            context = " ".join(lines[max(0, i-2):i+2])
            entry = _parse_turnitin_block(len(sources) + 1, [context])
            sources.append(entry)
    return sources


def turnitin_source_to_parsed(source: dict) -> dict:
    """Convierte una fuente Turnitin al formato dict que consume verify_reference()."""
    pct_label = f"  [{source['similarity_pct']}% similitud]" if source["similarity_pct"] else ""
    type_label = f"  [{source['source_type']}]" if source["source_type"] else ""
    raw_display = f"Fuente {source['number']}{pct_label}{type_label}: "
    if source["title"]:
        raw_display += source["title"]
    if source["url"]:
        raw_display += f"  URL: {source['url']}"

    return {
        "raw": raw_display,
        "doi": source.get("doi"),
        "year": source.get("year"),
        "title": source.get("title"),
        "authors": [],
        "_turnitin_similarity": source.get("similarity_pct"),
        "_source_type": source.get("source_type"),
        "_url": source.get("url"),
    }


def build_turnitin_report(results: list[dict], filename: str, total_sim: int | None) -> str:
    """Genera el informe Markdown para el modo --turnitin."""
    today = date.today().isoformat()
    total = len(results)
    counts = {s: sum(1 for r in results if r["status"] == s)
              for s in ["VERIFICADA", "POSIBLE", "SOSPECHOSA", "NO_ENCONTRADA"]}

    lines = []
    lines.append(f"# Verificación de Fuentes — Informe Turnitin\n")
    lines.append(f"**Archivo Turnitin analizado:** `{filename}`  ")
    if total_sim is not None:
        lines.append(f"**Similitud global reportada por Turnitin:** {total_sim}%  ")
    lines.append(f"**Fecha:** {today}  ")
    lines.append(f"**Fuentes procesadas:** {total}\n")
    lines.append("| Estado | Cantidad | % |")
    lines.append("|--------|----------|---|")
    for s, emoji in STATUS_EMOJI.items():
        pct = round(counts[s] / total * 100, 1) if total else 0
        lines.append(f"| {emoji} {s} | {counts[s]} | {pct}% |")
    lines.append("")

    # Resumen
    fraudulent = counts["SOSPECHOSA"] + counts["NO_ENCONTRADA"]
    if fraudulent == 0:
        summary = "Todas las fuentes reportadas por Turnitin fueron verificadas en bases de datos académicas. Las coincidencias detectadas corresponden a fuentes reales."
    elif fraudulent <= total * 0.1:
        summary = f"{fraudulent} fuente(s) no pudieron verificarse ({round(fraudulent/total*100)}%). Puede tratarse de fuentes institucionales internas, repositorios privados o errores de extracción del PDF."
    else:
        summary = f"⚠️ {fraudulent} de {total} fuentes ({round(fraudulent/total*100)}%) no tienen correspondencia verificable en bases de datos académicas abiertas. Esto puede indicar fuentes de acceso restringido, URLs rotas o URLs fabricadas."

    lines.append("## Resumen Ejecutivo\n")
    lines.append(summary)
    lines.append("")
    lines.append("---\n")
    lines.append("## Detalle por Fuente\n")

    for i, r in enumerate(results, 1):
        status = r["status"]
        emoji = STATUS_EMOJI[status]
        score = r["score"]
        turnitin_pct = r.get("_turnitin_similarity", "")
        source_type = r.get("_source_type", "")

        header_parts = [f"{emoji} {status} ({score}%  relevancia)"]
        if turnitin_pct:
            header_parts.append(f"Turnitin: {turnitin_pct}% similitud")
        if source_type:
            header_parts.append(source_type)

        lines.append(f"### {i}. {' · '.join(header_parts)}\n")
        lines.append(f"**Fuente Turnitin:**")
        lines.append(f"> {r['raw']}\n")

        bm = r.get("best_match")
        if bm:
            lines.append(f"**Verificada en:** {r['source']}  ")
            if bm.get("doi"):
                lines.append(f"**DOI:** https://doi.org/{bm['doi']}  ")
            lines.append(f"**Título en fuente:** {bm.get('title', 'N/A')}  ")
            if bm.get("year"):
                lines.append(f"**Año:** {bm['year']}  ")
            if bm.get("journal"):
                lines.append(f"**Revista:** {bm['journal']}  ")
        else:
            lines.append("**Resultado:** No encontrada en CrossRef, OpenAlex ni Semantic Scholar  ")

        if r.get("discrepancies"):
            lines.append("")
            lines.append("**⚠️ Observaciones:**")
            for d in r["discrepancies"]:
                lines.append(f"- {d}")

        lines.append("")

    lines.append("---\n")
    lines.append("*Generado por verificar_referencias.py · Modo Turnitin · APIs: CrossRef, OpenAlex, Semantic Scholar*")
    return "\n".join(lines)


# ─── Comparación de similitud ───────────────────────────────────────────────

def similarity(a: str, b: str) -> float:
    """Retorna similitud 0.0–1.0 entre dos cadenas (case-insensitive)."""
    if not a or not b:
        return 0.0
    a = re.sub(r"[^\w\s]", " ", a.lower())
    b = re.sub(r"[^\w\s]", " ", b.lower())
    return SequenceMatcher(None, a, b).ratio()


# ─── Consultas a APIs ──────────────────────────────────────────────────────

def check_doi(doi: str) -> bool:
    """Verifica si un DOI resuelve correctamente."""
    try:
        r = requests.head(
            f"https://doi.org/{doi}", allow_redirects=True, timeout=8
        )
        return r.status_code < 400
    except Exception:
        return False


def query_crossref(title: str, author: str = "", email: str = DEFAULT_EMAIL) -> list[dict]:
    """Busca en CrossRef por título (y opcionalmente autor)."""
    if not title:
        return []
    params = {
        "query.title": title,
        "rows": 5,
        "select": "DOI,title,author,published,score,container-title",
    }
    if author:
        params["query.author"] = author
    headers = {"User-Agent": f"VerificarRefs/1.0 (mailto:{email})"}
    try:
        r = requests.get(
            "https://api.crossref.org/works",
            params=params, headers=headers, timeout=12
        )
        if r.status_code == 200:
            items = r.json().get("message", {}).get("items", [])
            results = []
            for item in items:
                t = item.get("title", [""])[0] if item.get("title") else ""
                authors = [
                    f"{a.get('family', '')} {a.get('given', '')}".strip()
                    for a in item.get("author", [])
                ]
                pub_year = None
                if item.get("published"):
                    dp = item["published"].get("date-parts", [[None]])
                    pub_year = dp[0][0] if dp and dp[0] else None
                journal = item.get("container-title", [""])[0] if item.get("container-title") else ""
                results.append({
                    "source": "CrossRef",
                    "doi": item.get("DOI", ""),
                    "title": t,
                    "authors": authors,
                    "year": pub_year,
                    "journal": journal,
                    "api_score": item.get("score", 0),
                })
            return results
    except Exception as e:
        print(f"  AVISO CrossRef: {e}")
    return []


def query_openalex(title: str) -> list[dict]:
    """Busca en OpenAlex por título."""
    if not title:
        return []
    params = {"search": title, "per-page": 3, "select": "id,title,authorships,publication_year,primary_location,doi,relevance_score"}
    try:
        r = requests.get(
            "https://api.openalex.org/works",
            params=params, timeout=12
        )
        if r.status_code == 200:
            items = r.json().get("results", [])
            results = []
            for item in items:
                authors = [
                    a.get("author", {}).get("display_name", "")
                    for a in item.get("authorships", [])
                ]
                journal = ""
                loc = item.get("primary_location") or {}
                src = loc.get("source") or {}
                journal = src.get("display_name", "")
                doi = item.get("doi", "")
                if doi and doi.startswith("https://doi.org/"):
                    doi = doi[len("https://doi.org/"):]
                results.append({
                    "source": "OpenAlex",
                    "doi": doi,
                    "title": item.get("title") or "",
                    "authors": authors,
                    "year": item.get("publication_year"),
                    "journal": journal,
                    "api_score": item.get("relevance_score") or 0,
                })
            return results
    except Exception as e:
        print(f"  AVISO OpenAlex: {e}")
    return []


def query_semantic_scholar(title: str) -> list[dict]:
    """Busca en Semantic Scholar por título (fallback)."""
    if not title:
        return []
    params = {
        "query": title,
        "fields": "title,authors,year,externalIds,venue",
        "limit": 3,
    }
    try:
        r = requests.get(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            params=params, timeout=12
        )
        if r.status_code == 200:
            items = r.json().get("data", [])
            results = []
            for item in items:
                authors = [a.get("name", "") for a in item.get("authors", [])]
                doi = item.get("externalIds", {}).get("DOI", "")
                results.append({
                    "source": "Semantic Scholar",
                    "doi": doi,
                    "title": item.get("title") or "",
                    "authors": authors,
                    "year": item.get("year"),
                    "journal": item.get("venue") or "",
                    "api_score": 0,
                })
            return results
    except Exception as e:
        print(f"  AVISO Semantic Scholar: {e}")
    return []


# ─── Lógica de verificación ─────────────────────────────────────────────────

def verify_reference(parsed: dict, email: str = DEFAULT_EMAIL) -> dict:
    """Verifica una referencia contra las APIs y retorna el resultado."""
    result = {
        "raw": parsed["raw"],
        "status": "NO_ENCONTRADA",
        "score": 0,
        "best_match": None,
        "source": None,
        "doi_valid": False,
        "discrepancies": [],
    }

    # 1. Verificación directa por DOI
    if parsed.get("doi"):
        doi_ok = check_doi(parsed["doi"])
        result["doi_valid"] = doi_ok
        if doi_ok:
            result["status"] = "VERIFICADA"
            result["score"] = 100
            result["source"] = "DOI directo"
            result["best_match"] = {"doi": parsed["doi"], "title": "(DOI resuelto)", "year": parsed.get("year"), "authors": [], "journal": ""}
            return result
        else:
            result["discrepancies"].append(f"DOI declarado ({parsed['doi']}) no resuelve")

    # 2. Búsqueda por título
    title_query = parsed.get("title") or ""
    if len(title_query) < 10:
        result["status"] = "NO_ENCONTRADA"
        result["discrepancies"].append("No se pudo extraer el título de la referencia")
        return result

    # Buscar en CrossRef, luego OpenAlex, luego Semantic Scholar
    candidates = []
    candidates += query_crossref(title_query, email=email)
    time.sleep(PAUSE_BETWEEN_CALLS)
    if not candidates:
        candidates += query_openalex(title_query)
        time.sleep(PAUSE_BETWEEN_CALLS)
    if not candidates:
        candidates += query_semantic_scholar(title_query)
        time.sleep(PAUSE_BETWEEN_CALLS)

    if not candidates:
        return result

    # 3. Calcular score de similitud para cada candidato
    best = None
    best_score = 0
    for cand in candidates:
        title_sim = similarity(title_query, cand["title"]) * 100
        if title_sim > best_score:
            best_score = title_sim
            best = cand

    result["score"] = round(best_score)
    result["best_match"] = best
    result["source"] = best["source"] if best else None

    # 4. Verificar discrepancias en año
    if best and parsed.get("year") and best.get("year"):
        year_diff = abs(int(parsed["year"]) - int(best["year"]))
        if year_diff > 1:
            result["discrepancies"].append(
                f"Año declarado: {parsed['year']}  |  Año en fuente: {best['year']}"
            )

    # 5. Asignar estado
    if best_score >= MIN_SCORE_VERIFIED:
        if result["discrepancies"]:
            result["status"] = "SOSPECHOSA"
        else:
            result["status"] = "VERIFICADA"
    elif best_score >= MIN_SCORE_POSSIBLE:
        result["status"] = "POSIBLE"
    else:
        result["status"] = "NO_ENCONTRADA"

    # Año futuro = sospechosa siempre
    if parsed.get("year") and parsed["year"] > date.today().year:
        result["status"] = "SOSPECHOSA"
        result["discrepancies"].append(
            f"Año declarado ({parsed['year']}) es posterior al año actual"
        )

    return result


# ─── Generación del informe ─────────────────────────────────────────────────

STATUS_EMOJI = {
    "VERIFICADA":    "✅",
    "POSIBLE":       "🟡",
    "SOSPECHOSA":    "🔴",
    "NO_ENCONTRADA": "❌",
}

def build_report(results: list[dict], filename: str) -> str:
    today = date.today().isoformat()
    total = len(results)
    counts = {s: sum(1 for r in results if r["status"] == s)
              for s in ["VERIFICADA", "POSIBLE", "SOSPECHOSA", "NO_ENCONTRADA"]}

    lines = []
    lines.append(f"# Verificación de Referencias Bibliográficas\n")
    lines.append(f"**Archivo analizado:** `{filename}`  ")
    lines.append(f"**Fecha:** {today}  ")
    lines.append(f"**Total de referencias procesadas:** {total}\n")
    lines.append("| Estado | Cantidad | % |")
    lines.append("|--------|----------|---|")
    for s, emoji in STATUS_EMOJI.items():
        pct = round(counts[s] / total * 100, 1) if total else 0
        lines.append(f"| {emoji} {s} | {counts[s]} | {pct}% |")
    lines.append("")

    # Resumen ejecutivo
    suspicious = counts["SOSPECHOSA"] + counts["NO_ENCONTRADA"]
    if suspicious == 0:
        summary = "Todas las referencias verificadas tienen correspondencia en bases de datos académicas. No se detectaron indicios de referencias inventadas."
    elif suspicious <= total * 0.1:
        summary = f"Se detectaron {suspicious} referencia(s) que requieren revisión manual ({round(suspicious/total*100)}% del total). El resto tiene verificación satisfactoria."
    elif suspicious <= total * 0.3:
        summary = f"⚠️ Se detectaron {suspicious} referencias problemáticas ({round(suspicious/total*100)}%). Se recomienda revisar cada referencia marcada como SOSPECHOSA o NO ENCONTRADA antes de publicar el trabajo."
    else:
        summary = f"🚨 {suspicious} de {total} referencias ({round(suspicious/total*100)}%) no pudieron verificarse. Esto puede indicar referencias generadas por IA, errores tipográficos significativos o fuentes no indexadas. Se recomienda revisión exhaustiva."

    lines.append("## Resumen Ejecutivo\n")
    lines.append(summary)
    lines.append("")
    lines.append("---\n")
    lines.append("## Detalle por Referencia\n")

    for i, r in enumerate(results, 1):
        status = r["status"]
        emoji = STATUS_EMOJI[status]
        score = r["score"]
        lines.append(f"### {i}. {emoji} {status} ({score}%)\n")
        lines.append(f"**Referencia original:**")
        lines.append(f"> {r['raw']}\n")

        bm = r.get("best_match")
        if bm:
            lines.append(f"**Encontrada en:** {r['source']}  ")
            if bm.get("doi"):
                lines.append(f"**DOI:** https://doi.org/{bm['doi']}  ")
            lines.append(f"**Título en fuente:** {bm.get('title', 'N/A')}  ")
            if bm.get("authors"):
                lines.append(f"**Autores en fuente:** {'; '.join(bm['authors'][:3])}  ")
            if bm.get("year"):
                lines.append(f"**Año en fuente:** {bm['year']}  ")
            if bm.get("journal"):
                lines.append(f"**Revista/Fuente:** {bm['journal']}  ")
        else:
            lines.append("**Búsqueda en CrossRef, OpenAlex y Semantic Scholar:** sin resultados relevantes  ")

        if r.get("discrepancies"):
            lines.append("")
            lines.append("**⚠️ Discrepancias detectadas:**")
            for d in r["discrepancies"]:
                lines.append(f"- {d}")

        lines.append("")

    # Recomendaciones finales
    lines.append("---\n")
    lines.append("## Recomendaciones\n")
    not_found = [r for r in results if r["status"] == "NO_ENCONTRADA"]
    suspicious_list = [r for r in results if r["status"] == "SOSPECHOSA"]

    if not_found:
        lines.append("### Referencias no encontradas — acción sugerida")
        lines.append("Para cada referencia marcada como ❌ NO ENCONTRADA:")
        lines.append("1. Verificar manualmente en Google Scholar: https://scholar.google.com")
        lines.append("2. Si no se encuentra → podría ser una referencia inventada por IA")
        lines.append("3. Si se encuentra → el título puede tener errores tipográficos; corregir")
        lines.append("")

    if suspicious_list:
        lines.append("### Referencias sospechosas — acción sugerida")
        lines.append("Para cada referencia marcada como 🔴 SOSPECHOSA:")
        lines.append("1. Comparar año, autores y revista con la fuente encontrada")
        lines.append("2. Acceder al DOI encontrado y verificar que el contenido coincide con lo citado")
        lines.append("")

    lines.append("---")
    lines.append("*Generado por verificar_referencias.py · APIs: CrossRef, OpenAlex, Semantic Scholar*")

    return "\n".join(lines)


# ─── Comparación cruzada: Turnitin ↔ Bibliografía ──────────────────────────

def _extract_urls_from_text(text: str) -> list[str]:
    """Retorna lista de URLs normalizadas (sin protocolo, lowercase, sin trailing slash)."""
    urls = TURNITIN_URL.findall(text)
    normalized = []
    for u in urls:
        u = re.sub(r"^https?://", "", u).lower().rstrip("/.,;)")
        normalized.append(u)
    return normalized


def _url_domain(url: str) -> str:
    """Extrae el dominio/host de una URL ya normalizada."""
    return url.split("/")[0] if url else ""


def parse_turnitin_md_report(path: str) -> list[dict]:
    """
    Lee un informe TURNITIN-*.md ya generado y extrae sus entradas.
    Retorna lista de dicts: {num, raw, url, turnitin_pct, source_type, title}
    """
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    entries = []

    # Buscar bloques de sección: ### N. ...
    section_pat = re.compile(
        r"###\s+(\d+)\.\s+(.*?)\n\n\*\*Fuente Turnitin:\*\*\n>\s*(.*?)(?=\n\n###|\Z)",
        re.DOTALL
    )
    for m in section_pat.finditer(text):
        num = int(m.group(1))
        header = m.group(2)
        raw = m.group(3).strip()

        turnitin_pct = None
        pct_m = re.search(r"Turnitin:\s*(\d+)%", header)
        if pct_m:
            turnitin_pct = int(pct_m.group(1))

        source_type = None
        type_m = TURNITIN_SOURCE_TYPES.search(header)
        if type_m:
            source_type = type_m.group(0)

        url_m = TURNITIN_URL.search(raw)
        url = url_m.group(0).rstrip(".,;)") if url_m else None

        title = None
        title_m = re.search(r"Fuente\s+\d+.*?:\s+(.+?)(?:\s+URL:|$)", raw)
        if title_m:
            candidate = title_m.group(1).strip()
            if len(candidate) > 10 and not TURNITIN_URL.match(candidate):
                title = candidate

        entries.append({
            "num": num,
            "raw": raw,
            "url": url,
            "turnitin_pct": turnitin_pct or 0,
            "source_type": source_type or "",
            "title": title,
        })

    return entries


def parse_refs_md_report(path: str) -> list[dict]:
    """
    Lee un informe REFS-*.md ya generado y extrae sus entradas.
    Retorna lista de dicts: {num, raw, status, score, url, title}
    """
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    entries = []

    section_pat = re.compile(
        r"###\s+(\d+)\.\s+[✅🟡🔴❌]\s+(\w+)\s+\((\d+)%\)\n\n\*\*Referencia original:\*\*\n>\s*(.*?)(?=\n\n###|\Z)",
        re.DOTALL
    )
    for m in section_pat.finditer(text):
        num = int(m.group(1))
        status = m.group(2)
        score = int(m.group(3))
        raw = m.group(4).strip()

        url_m = TURNITIN_URL.search(raw)
        url = url_m.group(0).rstrip(".,;)") if url_m else None

        entries.append({
            "num": num,
            "raw": raw,
            "status": status,
            "score": score,
            "url": url,
        })

    return entries


def _urls_match(url_a: str | None, url_b: str | None) -> bool:
    """Comprueba si dos URLs apuntan al mismo recurso (por dominio + path prefix)."""
    if not url_a or not url_b:
        return False
    a = re.sub(r"^https?://", "", url_a).lower().rstrip("/.,;)")
    b = re.sub(r"^https?://", "", url_b).lower().rstrip("/.,;)")
    if a == b:
        return True
    # Match por handle numérico (hdl.handle.net/...)
    handle_a = re.search(r"handle\.net/(.+)", a)
    handle_b = re.search(r"handle\.net/(.+)", b)
    if handle_a and handle_b and handle_a.group(1) == handle_b.group(1):
        return True
    # Match por dominio compartido + al menos un segmento de path
    parts_a = [p for p in a.split("/") if p]
    parts_b = [p for p in b.split("/") if p]
    if parts_a and parts_b and parts_a[0] == parts_b[0] and len(parts_a) > 1 and len(parts_b) > 1:
        return parts_a[1] == parts_b[1]
    return False


def cross_reference(turnitin_entries: list[dict], refs_entries: list[dict]) -> list[dict]:
    """
    Cruza las fuentes Turnitin con las referencias del documento.
    Para cada fuente Turnitin determina si fue citada en la bibliografía.

    Clasificaciones:
    - BIEN_CITADA:         encontrada en bibliografía y verificada (VERIFICADA/POSIBLE)
    - CITADA_CON_PROBLEMA: encontrada en bibliografía pero con estado SOSPECHOSA/NO_ENCONTRADA
    - NO_CITADA:           no aparece en bibliografía
    """
    threshold_url = True   # match por URL
    threshold_title = 0.65 # similitud mínima de título para considerar match

    results = []
    for t_entry in turnitin_entries:
        matched_ref = None
        match_method = None

        for r_entry in refs_entries:
            # 1. Match por URL exacta / handle
            if _urls_match(t_entry.get("url"), r_entry.get("url")):
                matched_ref = r_entry
                match_method = "URL"
                break

            # 2. Match por dominio compartido en el texto raw de la referencia
            if t_entry.get("url"):
                t_domain = _url_domain(
                    re.sub(r"^https?://", "", t_entry["url"]).lower()
                )
                if t_domain and t_domain in r_entry["raw"].lower():
                    matched_ref = r_entry
                    match_method = "dominio"
                    break

            # 3. Match por similitud de título (si hay título extraído de Turnitin)
            if t_entry.get("title") and len(t_entry["title"]) > 15:
                sim = similarity(t_entry["title"], r_entry["raw"])
                if sim >= threshold_title:
                    matched_ref = r_entry
                    match_method = f"título ({round(sim*100)}%)"
                    break

        if matched_ref:
            ref_status = matched_ref.get("status", "")
            if ref_status in ("VERIFICADA", "POSIBLE"):
                classification = "BIEN_CITADA"
            else:
                classification = "CITADA_CON_PROBLEMA"
        else:
            classification = "NO_CITADA"

        results.append({
            "turnitin": t_entry,
            "matched_ref": matched_ref,
            "match_method": match_method,
            "classification": classification,
        })

    return results


def build_comparison_report(
    cross_results: list[dict],
    turnitin_file: str,
    refs_file: str,
    turnitin_global_sim: int | None,
) -> str:
    """Genera el informe Markdown de comparación cruzada."""
    today = date.today().isoformat()
    total = len(cross_results)

    counts = {c: sum(1 for r in cross_results if r["classification"] == c)
              for c in ["BIEN_CITADA", "CITADA_CON_PROBLEMA", "NO_CITADA"]}

    # Ponderado por % similitud de Turnitin para calcular riesgo real
    sim_no_citada = sum(
        r["turnitin"]["turnitin_pct"]
        for r in cross_results if r["classification"] == "NO_CITADA"
    )
    sim_total = sum(r["turnitin"]["turnitin_pct"] for r in cross_results) or 1
    risk_pct = round(sim_no_citada / sim_total * 100) if sim_total else 0

    lines = []
    lines.append("# Comparación Cruzada: Turnitin ↔ Bibliografía\n")
    lines.append(f"**Informe Turnitin:** `{turnitin_file}`  ")
    lines.append(f"**Informe de Referencias:** `{refs_file}`  ")
    if turnitin_global_sim is not None:
        lines.append(f"**Similitud global Turnitin:** {turnitin_global_sim}%  ")
    lines.append(f"**Fecha de análisis:** {today}  ")
    lines.append(f"**Fuentes Turnitin procesadas:** {total}\n")

    lines.append("| Clasificación | Cantidad | % fuentes |")
    lines.append("|---------------|----------|-----------|")
    icons = {"BIEN_CITADA": "✅", "CITADA_CON_PROBLEMA": "⚠️", "NO_CITADA": "❌"}
    for c, icon in icons.items():
        pct = round(counts[c] / total * 100, 1) if total else 0
        label = c.replace("_", " ").title()
        lines.append(f"| {icon} {label} | {counts[c]} | {pct}% |")
    lines.append("")

    # Resumen ejecutivo
    lines.append("## Resumen Ejecutivo\n")
    if counts["NO_CITADA"] == 0:
        lines.append("✅ **Todas las fuentes detectadas por Turnitin están citadas en la bibliografía.** "
                     "Las coincidencias son atribuidas correctamente.")
    elif risk_pct <= 10:
        lines.append(f"🟡 **Riesgo bajo.** {counts['NO_CITADA']} fuentes Turnitin no aparecen en la "
                     f"bibliografía, pero representan solo el {risk_pct}% del peso de similitud total. "
                     "Revisar y citar o parafrasear.")
    elif risk_pct <= 30:
        lines.append(f"⚠️ **Riesgo moderado.** {counts['NO_CITADA']} fuentes detectadas por Turnitin "
                     f"({risk_pct}% del peso de similitud) no están citadas en la bibliografía. "
                     "Se recomienda incorporar las citas faltantes o reescribir esos fragmentos.")
    else:
        lines.append(f"🚨 **Riesgo alto de plagio.** {counts['NO_CITADA']} fuentes detectadas por Turnitin "
                     f"representan el {risk_pct}% del peso de similitud y **no aparecen en la bibliografía**. "
                     "Es necesaria una revisión profunda del documento.")

    if counts["CITADA_CON_PROBLEMA"] > 0:
        lines.append(f"\n⚠️ Adicionalmente, {counts['CITADA_CON_PROBLEMA']} fuente(s) están citadas "
                     "pero con problemas de verificación (referencia sospechosa o no verificada en bases de datos).")

    lines.append("\n---\n")

    # Sección 1: NO CITADAS (prioridad alta, ordenadas por % similitud Turnitin desc)
    no_citadas = sorted(
        [r for r in cross_results if r["classification"] == "NO_CITADA"],
        key=lambda x: x["turnitin"]["turnitin_pct"],
        reverse=True
    )
    if no_citadas:
        lines.append("## ❌ Fuentes Turnitin NO citadas en la bibliografía\n")
        lines.append("> Estas fuentes generaron coincidencia de similitud pero no están referenciadas en el documento. "
                     "**Acción requerida: citar o eliminar el fragmento copiado.**\n")
        for r in no_citadas:
            t = r["turnitin"]
            pct_label = f"{t['turnitin_pct']}% similitud" if t["turnitin_pct"] else "?"
            type_label = f" · {t['source_type']}" if t["source_type"] else ""
            lines.append(f"- **Fuente {t['num']}** ({pct_label}{type_label})  ")
            if t.get("url"):
                lines.append(f"  URL: {t['url']}  ")
            if t.get("title"):
                lines.append(f"  Título: {t['title']}  ")
            lines.append("")
        lines.append("---\n")

    # Sección 2: CITADAS CON PROBLEMA
    con_problema = [r for r in cross_results if r["classification"] == "CITADA_CON_PROBLEMA"]
    if con_problema:
        lines.append("## ⚠️ Fuentes citadas pero con problemas de verificación\n")
        lines.append("> Estas fuentes están en la bibliografía pero la referencia tiene problemas "
                     "(año incorrecto, referencia no verificada, etc.).\n")
        for r in con_problema:
            t = r["turnitin"]
            ref = r["matched_ref"]
            pct_label = f"{t['turnitin_pct']}% similitud" if t["turnitin_pct"] else "?"
            ref_status = ref.get("status", "?") if ref else "?"
            status_icon = {"VERIFICADA": "✅", "POSIBLE": "🟡", "SOSPECHOSA": "🔴", "NO_ENCONTRADA": "❌"}.get(ref_status, "?")
            lines.append(f"- **Fuente Turnitin {t['num']}** ({pct_label})  ")
            lines.append(f"  Referencia #{ref['num']} en bibliografía → {status_icon} {ref_status}  ")
            if t.get("url"):
                lines.append(f"  URL: {t['url']}  ")
            lines.append(f"  Ref. original: {ref['raw'][:120]}...  ")
            lines.append(f"  *(Match por: {r['match_method']})*  ")
            lines.append("")
        lines.append("---\n")

    # Sección 3: BIEN CITADAS (resumen compacto)
    bien_citadas = [r for r in cross_results if r["classification"] == "BIEN_CITADA"]
    if bien_citadas:
        lines.append("## ✅ Fuentes Turnitin bien citadas en la bibliografía\n")
        lines.append(f"> {len(bien_citadas)} fuentes están correctamente referenciadas.\n")
        lines.append("| # Turnitin | Similitud | Match | # Ref bibliografía |")
        lines.append("|------------|-----------|-------|--------------------|")
        for r in bien_citadas:
            t = r["turnitin"]
            ref = r["matched_ref"]
            pct = f"{t['turnitin_pct']}%" if t["turnitin_pct"] else "-"
            ref_num = f"#{ref['num']}" if ref else "-"
            lines.append(f"| {t['num']} | {pct} | {r['match_method']} | {ref_num} |")
        lines.append("")

    lines.append("---\n")
    lines.append("*Generado por verificar_referencias.py · Modo Compare · Sin llamadas a APIs externas*")
    return "\n".join(lines)


# ─── Punto de entrada ──────────────────────────────────────────────────────

def main():
    global MIN_SCORE_VERIFIED

    parser = argparse.ArgumentParser(
        description="Verifica referencias bibliográficas contra CrossRef, OpenAlex y Semantic Scholar"
    )
    parser.add_argument("--file", required=False, default=None,
                        help="Ruta al archivo .docx, .pdf o .txt a analizar")
    parser.add_argument("--section", default=None, help="Nombre de la sección de referencias (ej: Bibliografía)")
    parser.add_argument("--email", default=DEFAULT_EMAIL, help="Email para el polite pool de CrossRef")
    parser.add_argument("--out", default="verificaciones", help="Carpeta de salida del informe")
    parser.add_argument("--min-score", type=int, default=MIN_SCORE_VERIFIED, help="Score mínimo para VERIFICADA")
    parser.add_argument("--turnitin", action="store_true",
                        help="Modo informe Turnitin: extrae y verifica las fuentes detectadas por Turnitin en el PDF")
    # Modo comparación
    parser.add_argument("--compare", action="store_true",
                        help="Cruza un informe TURNITIN-*.md con un informe REFS-*.md ya generados")
    parser.add_argument("--turnitin-report", default=None,
                        help="Ruta al informe TURNITIN-*.md (requerido con --compare)")
    parser.add_argument("--refs-report", default=None,
                        help="Ruta al informe REFS-*.md (requerido con --compare)")
    args = parser.parse_args()

    # Validaciones de combinaciones de flags
    if args.compare:
        if not args.turnitin_report or not args.refs_report:
            print("ERROR: --compare requiere --turnitin-report y --refs-report")
            sys.exit(1)
        if not os.path.exists(args.turnitin_report):
            print(f"ERROR: No se encuentra: {args.turnitin_report}")
            sys.exit(1)
        if not os.path.exists(args.refs_report):
            print(f"ERROR: No se encuentra: {args.refs_report}")
            sys.exit(1)
    else:
        if not args.file:
            print("ERROR: --file es requerido (o usa --compare con --turnitin-report y --refs-report)")
            sys.exit(1)
        if not os.path.exists(args.file):
            print(f"ERROR: No se encuentra el archivo: {args.file}")
            sys.exit(1)

    MIN_SCORE_VERIFIED = args.min_score

    mode_label = "Modo Turnitin" if args.turnitin else "Modo Bibliografía"
    if args.compare:
        mode_label = "Modo Compare"

    print(f"\n{'='*60}")
    print(f"  Verificador de Referencias Bibliográficas  [{mode_label}]")
    if args.compare:
        print(f"  Turnitin: {args.turnitin_report}")
        print(f"  Referencias: {args.refs_report}")
    else:
        print(f"  Archivo: {args.file}")
    print(f"{'='*60}\n")

    if args.compare:
        # ── MODO COMPARE ─────────────────────────────────────────────────
        print("📂 Leyendo informe Turnitin...")
        turnitin_entries = parse_turnitin_md_report(args.turnitin_report)
        print(f"   {len(turnitin_entries)} fuentes Turnitin leídas.")

        print("📂 Leyendo informe de referencias...")
        refs_entries = parse_refs_md_report(args.refs_report)
        print(f"   {len(refs_entries)} referencias leídas.\n")

        if not turnitin_entries:
            print("ERROR: No se pudieron extraer entradas del informe Turnitin.")
            sys.exit(1)

        # Detectar similitud global del encabezado del informe Turnitin
        turnitin_global_sim = None
        t_text = Path(args.turnitin_report).read_text(encoding="utf-8", errors="ignore")
        sim_m = re.search(r"Similitud global reportada por Turnitin:\*\*\s*(\d+)%", t_text)
        if sim_m:
            turnitin_global_sim = int(sim_m.group(1))

        print("🔗 Cruzando fuentes Turnitin con bibliografía del documento...")
        cross_results = cross_reference(turnitin_entries, refs_entries)

        counts = {c: sum(1 for r in cross_results if r["classification"] == c)
                  for c in ["BIEN_CITADA", "CITADA_CON_PROBLEMA", "NO_CITADA"]}
        print(f"   ✅ Bien citadas:           {counts['BIEN_CITADA']}")
        print(f"   ⚠️  Citadas con problema:   {counts['CITADA_CON_PROBLEMA']}")
        print(f"   ❌ No citadas:             {counts['NO_CITADA']}\n")

        print("📝 Generando informe de comparación...")
        report = build_comparison_report(
            cross_results,
            os.path.basename(args.turnitin_report),
            os.path.basename(args.refs_report),
            turnitin_global_sim,
        )

        os.makedirs(args.out, exist_ok=True)
        today_str = date.today().strftime("%Y%m%d")
        out_path = os.path.join(args.out, f"COMPARE-{today_str}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"\n{'='*60}")
        print(f"  COMPARACIÓN")
        print(f"{'='*60}")
        print(f"  ✅ Bien citadas:           {counts['BIEN_CITADA']}")
        print(f"  ⚠️  Citadas con problema:   {counts['CITADA_CON_PROBLEMA']}")
        print(f"  ❌ No citadas:             {counts['NO_CITADA']}")
        print(f"{'='*60}")
        print(f"\n  Informe guardado en: {out_path}\n")
        return

    # 1. Extraer texto
    print("📄 Extrayendo texto del archivo...")
    full_text = extract_text(args.file)
    print(f"   {len(full_text)} caracteres extraídos.\n")

    if args.turnitin:
        # ── MODO TURNITIN ──────────────────────────────────────────
        print("🔍 Extrayendo fuentes del informe Turnitin...")
        turnitin_sources = extract_turnitin_sources(full_text)
        print(f"   {len(turnitin_sources)} fuentes detectadas.\n")

        if not turnitin_sources:
            print("ERROR: No se detectaron fuentes en el informe Turnitin.")
            print("       Asegúrate de pasar el PDF completo del informe de similitud.")
            sys.exit(1)

        # Detectar % total de similitud Turnitin del encabezado
        total_sim = None
        sim_header = re.search(r"similarity\s+index[\s:]*([\d]+)\s*%", full_text, re.IGNORECASE)
        if sim_header:
            total_sim = int(sim_header.group(1))
        else:
            pct_matches = re.findall(r"([\d]{1,3})\s*%", full_text[:800])
            if pct_matches:
                total_sim = int(pct_matches[0])

        print(f"🌐 Verificando {len(turnitin_sources)} fuentes contra bases de datos académicas...\n")
        results = []
        for i, src in enumerate(turnitin_sources, 1):
            parsed = turnitin_source_to_parsed(src)
            title_preview = (parsed.get("title") or parsed["raw"])[:65]
            print(f"  [{i}/{len(turnitin_sources)}] {title_preview}...")
            result = verify_reference(parsed, email=args.email)
            # Preservar metadatos Turnitin en el resultado
            result["_turnitin_similarity"] = parsed.get("_turnitin_similarity")
            result["_source_type"] = parsed.get("_source_type")
            results.append(result)
            status_icon = STATUS_EMOJI.get(result["status"], "?")
            print(f"         → {status_icon} {result['status']} ({result['score']}%)")

        print(f"\n📝 Generando informe...")
        report = build_turnitin_report(results, os.path.basename(args.file), total_sim)

        os.makedirs(args.out, exist_ok=True)
        today_str = date.today().strftime("%Y%m%d")
        base_name = Path(args.file).stem.replace(" ", "_")
        out_path = os.path.join(args.out, f"TURNITIN-{base_name}-{today_str}.md")

    else:
        # ── MODO BIBLIOGRAFÍA (original) ───────────────────────────
        # 2. Encontrar sección de referencias
        print("🔍 Localizando sección de referencias...")
        section_text = find_references_section(full_text, section_hint=args.section)
        print(f"   Bloque de referencias: {len(section_text)} caracteres.\n")

        # 3. Dividir en referencias individuales
        print("📋 Dividiendo en referencias individuales...")
        raw_refs = split_references(section_text)
        print(f"   {len(raw_refs)} referencias detectadas.\n")

        if not raw_refs:
            print("ERROR: No se encontraron referencias. Verifica que el archivo tiene una sección de bibliografía.")
            sys.exit(1)

        # 4. Parsear y verificar
        print(f"🌐 Verificando contra bases de datos académicas...\n")
        results = []
        for i, raw in enumerate(raw_refs, 1):
            parsed = parse_reference(raw)
            title_preview = (parsed.get("title") or raw)[:60]
            print(f"  [{i}/{len(raw_refs)}] {title_preview}...")
            result = verify_reference(parsed, email=args.email)
            results.append(result)
            status_icon = STATUS_EMOJI.get(result["status"], "?")
            print(f"         → {status_icon} {result['status']} ({result['score']}%)")

        # 5. Generar informe
        print(f"\n📝 Generando informe...")
        report = build_report(results, os.path.basename(args.file))

        os.makedirs(args.out, exist_ok=True)
        today_str = date.today().strftime("%Y%m%d")
        base_name = Path(args.file).stem.replace(" ", "_")
        out_path = os.path.join(args.out, f"REFS-{base_name}-{today_str}.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    # Resumen final
    counts = {"VERIFICADA": 0, "POSIBLE": 0, "SOSPECHOSA": 0, "NO_ENCONTRADA": 0}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    print(f"\n{'='*60}")
    print(f"  RESULTADOS")
    print(f"{'='*60}")
    print(f"  ✅ VERIFICADAS:     {counts['VERIFICADA']}")
    print(f"  🟡 POSIBLES:        {counts['POSIBLE']}")
    print(f"  🔴 SOSPECHOSAS:     {counts['SOSPECHOSA']}")
    print(f"  ❌ NO ENCONTRADAS:  {counts['NO_ENCONTRADA']}")
    print(f"{'='*60}")
    print(f"\n  Informe guardado en: {out_path}\n")


if __name__ == "__main__":
    main()
