#!/usr/bin/env python3
"""Validate the v0.10.0 release and write machine-readable QA outputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import pandas as pd
from PIL import Image
from pypdf import PdfReader

from build_v010 import extract_author_letter


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BASELINE_SHA256 = "dc5f5348f5f82f78ec252cbc607703543f7186702bea790c6606c329e30749dc"
DEFAULT_PDF = ROOT / "reports/ELECTRICIDAD_ARGENTINA_v0.10.0_REVISION_AUTOR.pdf"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


def add(results: list[dict], check: str, status: str, detail: str) -> None:
    results.append({"check": check, "status": status, "detail": detail})


def verify_baseline(path: Path, results: list[dict]) -> None:
    if not path.exists():
        add(results, "baseline_external", "FAIL", f"No existe: {path}")
        return
    digest = sha256(path)
    add(results, "baseline_sha256", "PASS" if digest == EXPECTED_BASELINE_SHA256 else "FAIL", digest)
    try:
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
            names = zf.namelist()
            add(results, "baseline_zip_integrity", "PASS" if bad is None else "FAIL", f"entries={len(names)}; bad={bad}")
            manifest_names = [n for n in names if n.endswith("/MANIFEST.sha256") or n == "MANIFEST.sha256"]
            if not manifest_names:
                add(results, "baseline_internal_manifest", "FAIL", "MANIFEST.sha256 ausente")
                return
            manifest_name = manifest_names[0]
            prefix = manifest_name[: -len("MANIFEST.sha256")]
            lines = zf.read(manifest_name).decode("utf-8").splitlines()
            mismatches = []
            checked = 0
            for line in lines:
                if not line.strip():
                    continue
                expected, rel = line.split(None, 1)
                rel = rel.strip().lstrip("*").removeprefix("./")
                member = prefix + rel
                if member == manifest_name:
                    continue
                try:
                    actual = hashlib.sha256(zf.read(member)).hexdigest()
                except KeyError:
                    mismatches.append(f"missing:{rel}")
                    continue
                checked += 1
                if actual != expected:
                    mismatches.append(rel)
            add(results, "baseline_internal_manifest", "PASS" if not mismatches else "FAIL", f"checked={checked}; mismatches={len(mismatches)}")
    except Exception as exc:
        add(results, "baseline_zip_integrity", "FAIL", str(exc))


def pdf_font_audit(reader: PdfReader) -> tuple[dict[str, bool], int]:
    fonts: dict[str, bool] = {}
    links = 0
    for page in reader.pages:
        resources = page.get("/Resources", {})
        for ref in resources.get("/Font", {}).values():
            font = ref.get_object()
            name = str(font.get("/BaseFont", "UNKNOWN"))
            embedded = False
            descriptors = []
            if font.get("/FontDescriptor"):
                descriptors.append(font["/FontDescriptor"].get_object())
            for descendant in font.get("/DescendantFonts", []):
                dfont = descendant.get_object()
                if dfont.get("/FontDescriptor"):
                    descriptors.append(dfont["/FontDescriptor"].get_object())
            for descriptor in descriptors:
                embedded = embedded or any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
            fonts[name] = fonts.get(name, False) or embedded
        for annot in page.get("/Annots", []):
            if annot.get_object().get("/Subtype") == "/Link":
                links += 1
    return fonts, links


def extract_pdf_letter(reader: PdfReader) -> str:
    chunks = []
    for page in reader.pages[1:6]:
        text = page.extract_text() or ""
        for token in (
            "ELECTRICIDAD ARGENTINA · CAMBIO, LÍMITES Y DECISIONES",
            "REVISIÓN DEL AUTOR",
            "TGCP v0.10.0",
            "Carta del autor:",
        ):
            text = text.replace(token, "")
        text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
        chunks.append(text)
        if "Sebastián Liscia." in text:
            break
    combined = "\n".join(chunks)
    end = combined.find("Sebastián Liscia.")
    return combined[: end + len("Sebastián Liscia.")] if end >= 0 else combined


def validate_pdf(pdf: Path, results: list[dict]) -> tuple[PdfReader, str]:
    if not pdf.exists():
        add(results, "pdf_exists", "FAIL", str(pdf))
        raise FileNotFoundError(pdf)
    reader = PdfReader(str(pdf))
    add(results, "pdf_pages", "PASS" if 40 <= len(reader.pages) <= 100 else "FAIL", str(len(reader.pages)))
    a4 = True
    portrait = True
    for page in reader.pages:
        w, h = float(page.mediabox.width), float(page.mediabox.height)
        a4 = a4 and abs(w - 595.276) < 1.0 and abs(h - 841.89) < 1.0
        portrait = portrait and h > w
    add(results, "pdf_a4", "PASS" if a4 else "FAIL", "all pages")
    add(results, "pdf_portrait", "PASS" if portrait else "FAIL", "all pages")
    metadata = reader.metadata or {}
    add(results, "pdf_metadata_title", "PASS" if metadata.get("/Title") == "Electricidad argentina: cambio, límites y decisiones" else "FAIL", str(metadata.get("/Title")))
    add(results, "pdf_metadata_author", "PASS" if metadata.get("/Author") == "Sebastián Liscia" else "FAIL", str(metadata.get("/Author")))

    fonts, links = pdf_font_audit(reader)
    missing = sorted(name for name, embedded in fonts.items() if not embedded)
    add(results, "pdf_fonts_embedded", "PASS" if not missing else "FAIL", f"fonts={len(fonts)}; not_embedded={missing}")
    add(results, "pdf_links", "PASS" if links >= 20 else "FAIL", str(links))
    outline = reader.outline
    add(results, "pdf_bookmarks", "PASS" if len(outline) >= 15 else "FAIL", str(len(outline)))

    pages_text = [page.extract_text() or "" for page in reader.pages]
    full_text = "\n".join(pages_text)
    add(results, "pdf_selectable_text", "PASS" if len(full_text) > 50000 else "FAIL", f"characters={len(full_text)}")
    add(results, "front_order_letter", "PASS" if pages_text[1].lstrip().startswith("Carta del autor:") else "FAIL", pages_text[1][:60].replace("\n", " "))
    letter_marked, reference_letter = extract_author_letter(ROOT / "editorial/source/Carta_autor_original.odt")
    del letter_marked
    letter_pdf = extract_pdf_letter(reader)
    add(results, "author_letter_literal", "PASS" if normalized(letter_pdf) == normalized(reference_letter) else "FAIL", f"reference_chars={len(normalized(reference_letter))}; pdf_chars={len(normalized(letter_pdf))}")

    toc_pos = full_text.find("Índice")
    ch1_pos = full_text.find("1. Qué cambió en el sistema eléctrico argentino")
    add(results, "front_order_toc_before_body", "PASS" if 0 <= toc_pos < ch1_pos else "FAIL", f"toc={toc_pos}; chapter1={ch1_pos}")
    literal = "El análisis económico-financiero ampliado no se desarrolla por decisión del autor."
    add(results, "required_scope_sentence", "PASS" if full_text.count(literal) == 1 else "FAIL", f"count={full_text.count(literal)}")

    chapter_titles = [
        "1. Qué cambió en el sistema eléctrico argentino",
        "2. Alcance, fuentes y fronteras",
        "3. Demanda, punta y flexibilidad",
        "4. La incorporación de las renovables",
        "5. Agua y generación hidráulica",
        "6. Generación térmica, emisiones y respuesta horaria",
        "7. Territorio, red y capacidades tecnológicas",
        "8. Argentina frente a Brasil, Chile y Uruguay",
        "9. Del diagnóstico a las decisiones",
        "10. Conclusión integrada",
        "11. Límites y agenda de datos",
    ]
    missing_chapters = [title for title in chapter_titles if full_text.count(title) < 2]  # TOC + heading
    add(results, "eleven_chapters", "PASS" if not missing_chapters else "FAIL", f"missing={missing_chapters}")
    add(results, "buenos_aires_literal", "PASS" if "BUENOS AIRES" in full_text else "FAIL", "literal category present")

    raw_patterns = [r"\{\{", r"\[CAM_[A-Z0-9_]+\]", r"/mnt/", r"\.csv\b", r"\.xlsx\b", r"\.md\b", r"GO_BOUNDED", r"VERIFIED\b"]
    hits = [pattern for pattern in raw_patterns if re.search(pattern, full_text)]
    add(results, "pdf_no_raw_tokens_or_filenames", "PASS" if not hits else "FAIL", f"hits={hits}")
    forbidden = [r"\bCAPEX\b", r"\bOPEX\b", r"\bWACC\b", r"\bVAN\b", r"\bTIR\b", r"\bLCOE\b", r"\bPPA\b", r"\bTFI\b", r"centro de datos"]
    forbidden_hits = [pattern for pattern in forbidden if re.search(pattern, full_text, re.I)]
    add(results, "scope_forbidden_sections_absent", "PASS" if not forbidden_hits else "FAIL", f"hits={forbidden_hits}")
    return reader, full_text


def figure_audit(results: list[dict], full_text: str, write: bool) -> None:
    source = (ROOT / "editorial/source/INFORME_v0.10.0.md").read_text(encoding="utf-8")
    with (ROOT / "figures/FIGURE_PUBLICATION_REGISTER_v0.10.0.csv").open(encoding="utf-8", newline="") as fh:
        register = list(csv.DictReader(fh))
    add(results, "figure_count", "PASS" if len(register) == 28 else "FAIL", str(len(register)))
    maps = [row for row in register if row["map_flag"] == "YES"]
    add(results, "map_count", "PASS" if len(maps) == 4 else "FAIL", str(len(maps)))
    audit_rows = []
    failures = []
    for row in register:
        fid = row["figure_id"]
        directive = f"{{{{FIG:{fid}}}}}"
        source_count = source.count(directive)
        label = "Mapa" if row["map_flag"] == "YES" else "Figura"
        # Each caption appears once in the body and once in the combined
        # figures/tables list at the end of the PDF.
        pdf_count = full_text.count(f"{label} {fid}.")
        pos = source.find(directive)
        next_pos = source.find("{{FIG:", pos + len(directive))
        segment = source[pos : next_pos if next_pos >= 0 else len(source)] if pos >= 0 else ""
        lower = segment.lower()
        how = any(term in lower for term in (
            "se lee", "lectura", "representa", "muestra", "barras", "líneas", "puntos",
            "panel", "columna", "curva", "áreas", "puente", "tarjetas", "trazos",
            "símbolos", "coeficientes", "índice", "figura", "mapa",
        ))
        pattern = any(term in lower for term in (
            "patrón", "muestra", "divergencia", "trayectoria", "permanece", "persistencia",
            "dominante", "mayoritario", "heterogéneo", "estable", "descienden", "crece",
            "expansión", "cambio", "distancia", "diferencia", "suma", "separa", "combina",
            "superpone",
        ))
        meaning = any(term in lower for term in (
            "significado", "implicancia", "implica", "importa", "resultado", "indica", "confirma",
            "explica", "útil", "valor", "permite", "obliga", "requiere", "relevancia",
        ))
        relevance = any(term in lower for term in (
            "relevancia", "estratég", "decisión", "operativ", "planificación", "política",
            "gestión", "prioridad", "implicancia", "importa", "utilidad", "valor",
            "para decisiones", "para la estrategia", "para el sistema",
        ))
        limit = any(term in lower for term in ("límite", "no ", "tampoco", "oculta", "sin "))
        image_path = ROOT / row["png"]
        legible = False
        try:
            with Image.open(image_path) as im:
                im.load()
                legible = min(im.size) >= 1400 and (im.width * im.height) >= 3_000_000
        except Exception:
            legible = False
        status = "PASS" if all((source_count == 1, pdf_count >= 2, how, pattern, meaning, relevance, limit, legible, row["publication_status"] == "PASS")) else "FAIL"
        if status == "FAIL":
            failures.append(fid)
        audit_rows.append(
            {
                "figure_id": fid,
                "cited_in_text": "YES" if source_count == 1 and pdf_count >= 2 else "NO",
                "how_to_read_present": "YES" if how else "NO",
                "pattern_explained": "YES" if pattern else "NO",
                "meaning_explained": "YES" if meaning else "NO",
                "strategic_relevance_explained": "YES" if relevance else "NO",
                "limit_explained": "YES" if limit else "NO",
                "numeric_parity": "PASS" if row["publication_status"] == "PASS" else "FAIL",
                "visual_legibility": "PASS" if legible else "FAIL",
                "status": status,
            }
        )
    add(results, "figure_interpretation_complete", "PASS" if not failures else "FAIL", f"failures={failures}")
    if write:
        path = ROOT / "qa/FIGURE_INTERPRETATION_AUDIT_v0.10.0.csv"
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(audit_rows[0].keys()))
            writer.writeheader()
            writer.writerows(audit_rows)


def data_checks(results: list[dict]) -> None:
    metrics = pd.read_csv(ROOT / "science/CANONICAL_METRICS_v0.10.0.csv")
    add(results, "canonical_metrics_present", "PASS" if len(metrics) >= 20 else "FAIL", f"rows={len(metrics)}")

    reg = pd.read_csv(ROOT / "regional/REGIONAL_NORMALIZED_METRICS_v0.10.0.csv")
    structural_zero = reg[(reg["country_es"].isin(["Chile", "Uruguay"])) & reg["nuclear_twh"].eq(0)]
    add(results, "regional_structural_nuclear_zeros", "PASS" if len(structural_zero) == 16 else "FAIL", f"rows={len(structural_zero)}")

    scenarios = pd.read_csv(ROOT / "scenarios/SCENARIO_SENSITIVITY_RESULTS_v0.10.0.csv")
    scenario_ok = len(scenarios) == 4 and scenarios["dispatch_feasibility"].eq("NOT_TESTED").all() and scenarios["storage_curtailment_network_commitment"].eq("NOT_MODELED").all()
    add(results, "scenario_boundary", "PASS" if scenario_ok else "FAIL", f"rows={len(scenarios)}")

    nodes = pd.read_csv(ROOT / "network/NODE_CROSSWALK_v0.10.0.csv")
    counts = nodes["match_status"].value_counts().to_dict()
    expected = {
        "MATCHED_SPATIAL_AND_NAME": 94,
        "MATCHED_SPATIAL_ONLY": 6,
        "NO_CONFIDENT_MATCH": 308,
        "MISSING_COORDINATES": 3,
    }
    add(results, "node_crosswalk_counts", "PASS" if all(counts.get(k, 0) == v for k, v in expected.items()) else "FAIL", json.dumps(counts, ensure_ascii=False, sort_keys=True))

    figure_pngs = sorted((ROOT / "figures/png").glob("*.png"))
    bad = []
    for path in figure_pngs:
        try:
            with Image.open(path) as im:
                im.load()
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    add(results, "figure_png_integrity", "PASS" if len(figure_pngs) == 28 and not bad else "FAIL", f"count={len(figure_pngs)}; bad={bad}")


def manifest_check(results: list[dict]) -> None:
    path = ROOT / "MANIFEST.sha256"
    if not path.exists():
        add(results, "release_manifest", "NOT_APPLICABLE", "manifest not generated yet")
        return
    mismatches = []
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for line in lines:
        expected, rel = line.split(None, 1)
        rel = rel.strip().lstrip("*")
        target = ROOT / rel
        if not target.exists() or sha256(target) != expected:
            mismatches.append(rel)
    physical = sum(1 for p in ROOT.rglob("*") if p.is_file())
    count_ok = physical == len(lines) + 1
    add(results, "release_manifest", "PASS" if not mismatches and count_ok else "FAIL", f"listed={len(lines)}; physical={physical}; mismatches={len(mismatches)}")


def active_fail_scan(results: list[dict]) -> None:
    active = []
    for path in sorted((ROOT / "qa").glob("*.csv")):
        try:
            df = pd.read_csv(path, dtype=str).fillna("")
        except Exception:
            continue
        for col in df.columns:
            if col.lower() in {"status", "estado", "final_status"}:
                if df[col].str.fullmatch("FAIL", case=False).any():
                    active.append(path.name)
    add(results, "zero_active_fail", "PASS" if not active else "FAIL", f"files={active}")


def write_reports(results: list[dict]) -> None:
    qa = ROOT / "qa"
    qa.mkdir(exist_ok=True)
    report = {
        "version": "v0.10.0",
        "status": "PASS" if not any(row["status"] == "FAIL" for row in results) else "FAIL",
        "checks": results,
    }
    (qa / "VALIDATION_REPORT_v0.10.0.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {status: sum(row["status"] == status for row in results) for status in ("PASS", "PASS_WITH_LIMITATION", "NOT_APPLICABLE", "FAIL")}
    lines = [
        "# Resumen de validación v0.10.0",
        "",
        f"Estado general: **{report['status']}**.",
        "",
        f"Controles: {counts['PASS']} PASS; {counts['PASS_WITH_LIMITATION']} PASS_WITH_LIMITATION; {counts['NOT_APPLICABLE']} NOT_APPLICABLE; {counts['FAIL']} FAIL.",
        "",
        "| Control | Estado | Detalle |",
        "|---|---|---|",
    ]
    for row in results:
        detail = str(row["detail"]).replace("|", "\\|")
        lines.append(f"| {row['check']} | {row['status']} | {detail} |")
    (qa / "VALIDATION_SUMMARY_v0.10.0.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-zip", type=Path)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--check-only", action="store_true", help="Do not rewrite QA outputs")
    args = parser.parse_args()

    results: list[dict] = []
    if args.baseline_zip:
        verify_baseline(args.baseline_zip.resolve(), results)
    else:
        add(results, "baseline_external", "NOT_APPLICABLE", "provide --baseline-zip for external verification")
    try:
        _, full_text = validate_pdf(args.pdf.resolve(), results)
    except Exception as exc:
        add(results, "pdf_validation", "FAIL", str(exc))
        full_text = ""
    figure_audit(results, full_text, write=not args.check_only)
    data_checks(results)
    manifest_check(results)
    active_fail_scan(results)
    if not args.check_only:
        write_reports(results)

    for row in results:
        print(f"{row['status']:20s} {row['check']}: {row['detail']}")
    failures = [row for row in results if row["status"] == "FAIL"]
    print(f"SUMMARY PASS={sum(r['status']=='PASS' for r in results)} FAIL={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
