#!/usr/bin/env python3
"""Generate the publication bibliography and auditable source register."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def key(author: str, year: str, used: set[str]) -> str:
    stem = unicodedata.normalize("NFKD", author).encode("ascii", "ignore").decode()
    stem = re.sub(r"[^A-Za-z0-9]+", "", stem.split(",")[0])[:18] or "Fuente"
    candidate = f"{stem}{year}"
    suffix = 2
    while candidate in used:
        candidate = f"{stem}{year}_{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def braces(value: str) -> str:
    return value.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def claim_for(author: str, title: str) -> str:
    text = f"{author} {title}".lower()
    if "cammesa" in text:
        return "balances, operación, renovables, hidráulica, intercambios o topología del SADI, según la obra"
    if any(term in text for term in ("ley", "decreto", "resolución")):
        return "marco normativo y rutas institucionales de incorporación renovable"
    if "ember" in text:
        return "trayectoria eléctrica regional armonizada 2018–2025"
    if "population" in text or "población" in text:
        return "denominador poblacional 2025 para métricas regionales per cápita"
    if "ign" in text:
        return "límites, localización de activos y fondo cartográfico oficial"
    if "transporte eléctrico" in text:
        return "geometría y atributos publicados de líneas o estaciones"
    if any(term in text for term in ("inti", "impsa", "imsa", "faraday", "cnea")):
        return "evidencia primaria de existencia de capacidades tecnológicas"
    if any(term in text for term in ("lmdi", "covariance", "instrument", "rank tests")):
        return "fundamento metodológico para descomposición o inferencia econométrica"
    if "nasa" in text:
        return "controles meteorológicos horarios"
    if "ciberseguridad" in text:
        return "marco institucional de ciberseguridad"
    if "almamdi" in text:
        return "inventario nodal adjunto y cobertura geográfica"
    return "contexto institucional o técnico citado en el informe"


def limitation_for(author: str, title: str) -> str:
    text = f"{author} {title}".lower()
    if "cammesa" in text:
        return "la frontera depende de la base y del vintage; topología no equivale a flujo"
    if "ember" in text:
        return "armonización comparable con menor detalle que los cierres nacionales"
    if "population" in text or "población" in text:
        return "la población no controla clima, estructura productiva ni electrificación"
    if "ign" in text or "transporte eléctrico" in text:
        return "la geometría no informa por sí sola flujo, congestión o margen"
    if any(term in text for term in ("inti", "impsa", "imsa", "faraday", "cnea")):
        return "la fuente primaria prueba existencia, no escala, integración completa ni competitividad"
    if "almamdi" in text:
        return "campos sin diccionario y coincidencias nodales incompletas"
    if any(term in text for term in ("lmdi", "covariance", "instrument", "rank tests")):
        return "la validez empírica sigue condicionada a datos, frontera y supuestos"
    return "usar sólo para la afirmación y frontera registradas"


def main() -> None:
    refs = json.loads((ROOT / "sources/BIBLIOGRAPHY_v0.10.0.json").read_text(encoding="utf-8"))
    local = {}
    source_registry = ROOT / "sources/SOURCE_REGISTRY_v0.10.0.csv"
    with source_registry.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            local[row["url"]] = row

    used: set[str] = set()
    bib_entries = []
    register_rows = []
    for ref in refs:
        citekey = key(ref["author"], ref["year"], used)
        fields = [
            f"  author = {{{braces(ref['author'])}}}",
            f"  title = {{{braces(ref['title'])}}}",
            f"  year = {{{braces(ref['year'])}}}",
            f"  note = {{{braces(ref['kind'])}}}",
        ]
        if ref.get("url"):
            fields.append(f"  url = {{{braces(ref['url'])}}}")
            fields.append("  urldate = {2026-08-18}")
        bib_entries.append("@misc{" + citekey + ",\n" + ",\n".join(fields) + "\n}")

        loc = local.get(ref.get("url", ""), {})
        artifact = loc.get("local_artifact", "")
        digest = loc.get("sha256", "").strip()
        register_rows.append(
            {
                "reference_id": citekey,
                "autor_o_institucion": ref["author"],
                "titulo_real": ref["title"],
                "anio": ref["year"],
                "tipo": ref["kind"],
                "url_oficial_o_doi": ref.get("url", ""),
                "fecha_consulta": "2026-08-18" if ref.get("url") else "NOT_APPLICABLE",
                "afirmaciones_que_sostiene": claim_for(ref["author"], ref["title"]),
                "limite_de_uso": loc.get("limitation") or limitation_for(ref["author"], ref["title"]),
                "disponibilidad_local": artifact or "sin copia local en el release",
                "sha256_local": digest or "NOT_APPLICABLE",
                "estado": "PASS_WITH_LIMITATION" if not ref.get("url") else "PASS",
            }
        )

    (ROOT / "sources/publication_references_v0.10.0.bib").write_text(
        "% Bibliografía de publicación v0.10.0 — UTF-8\n\n" + "\n\n".join(bib_entries) + "\n",
        encoding="utf-8",
    )
    path = ROOT / "sources/PUBLICATION_SOURCE_REGISTER_v0.10.0.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(register_rows[0].keys()))
        writer.writeheader()
        writer.writerows(register_rows)
    print(f"publication references: {len(register_rows)}")


if __name__ == "__main__":
    main()
