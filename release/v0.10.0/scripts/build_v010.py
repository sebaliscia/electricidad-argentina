#!/usr/bin/env python3
"""Build the complete Spanish A4 author-review PDF for TGCP v0.10.0.

The canonical narrative is editorial/source/INFORME_v0.10.0.md. The author
letter is extracted directly from the original ODT at build time, preserving
its visible text, paragraph breaks, manual line breaks, italics and signature.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    LongTable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
PAGE_W, PAGE_H = A4
SOURCE = ROOT / "editorial/source/INFORME_v0.10.0.md"
LETTER_ODT = ROOT / "editorial/source/Carta_autor_original.odt"
TABLES_PATH = ROOT / "editorial/source/TABLES_v0.10.0.json"
BIB_PATH = ROOT / "sources/BIBLIOGRAPHY_v0.10.0.json"
TOKENS_PATH = ROOT / "editorial/styles/DESIGN_TOKENS_v0.10.0.json"
REGISTER_PATH = ROOT / "figures/FIGURE_PUBLICATION_REGISTER_v0.10.0.csv"

TOKENS = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
TABLES = json.loads(TABLES_PATH.read_text(encoding="utf-8"))
BIBLIOGRAPHY = json.loads(BIB_PATH.read_text(encoding="utf-8"))

NAVY = colors.HexColor(TOKENS["colors"]["navy"])
TEAL = colors.HexColor(TOKENS["colors"]["teal"])
MINT = colors.HexColor(TOKENS["colors"]["mint"])
GOLD = colors.HexColor(TOKENS["colors"]["gold"])
ORANGE = colors.HexColor(TOKENS["colors"]["orange"])
INK = colors.HexColor(TOKENS["colors"]["ink"])
GREY = colors.HexColor(TOKENS["colors"]["grey"])
LIGHT = colors.HexColor(TOKENS["colors"]["light"])

LEFT = TOKENS["page"]["margin_left_mm"] * mm
RIGHT = TOKENS["page"]["margin_right_mm"] * mm
TOP = TOKENS["page"]["margin_top_mm"] * mm
BOTTOM = TOKENS["page"]["margin_bottom_mm"] * mm
BODY_W = PAGE_W - LEFT - RIGHT
BODY_H = PAGE_H - TOP - BOTTOM


def register_fonts() -> None:
    font_dir = ROOT / "editorial/fonts"
    fonts = {
        "SourceSerif": "SourceSerif4_400Regular.ttf",
        "SourceSerif-Italic": "SourceSerif4_400Regular_Italic.ttf",
        "SourceSerif-Semibold": "SourceSerif4_600SemiBold.ttf",
        "SourceSerif-Bold": "SourceSerif4_700Bold.ttf",
        "SourceSans": "SourceSans3_400Regular.ttf",
        "SourceSans-Italic": "SourceSans3_400Regular_Italic.ttf",
        "SourceSans-Semibold": "SourceSans3_600SemiBold.ttf",
        "SourceSans-Bold": "SourceSans3_700Bold.ttf",
    }
    for name, filename in fonts.items():
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily(
        "SourceSerif",
        normal="SourceSerif",
        bold="SourceSerif-Bold",
        italic="SourceSerif-Italic",
        boldItalic="SourceSerif-Italic",
    )
    pdfmetrics.registerFontFamily(
        "SourceSans",
        normal="SourceSans",
        bold="SourceSans-Bold",
        italic="SourceSans-Italic",
        boldItalic="SourceSans-Italic",
    )


def styles() -> dict[str, ParagraphStyle]:
    body_size = TOKENS["body"]["size_pt"]
    body_leading = TOKENS["body"]["leading_pt"]
    return {
        "body": ParagraphStyle(
            "Body",
            fontName="SourceSerif",
            fontSize=body_size,
            leading=body_leading,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=4.4,
            allowWidows=0,
            allowOrphans=0,
            splitLongWords=False,
            hyphenationLang="es_ES",
        ),
        "letter": ParagraphStyle(
            "Letter",
            fontName="SourceSerif",
            fontSize=8.9,
            leading=11.45,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=5.2,
            allowWidows=0,
            allowOrphans=0,
            splitLongWords=False,
            hyphenationLang="es_ES",
        ),
        "letter_heading": ParagraphStyle(
            "LetterHeading",
            fontName="SourceSans-Bold",
            fontSize=19,
            leading=22,
            textColor=NAVY,
            spaceAfter=10,
            keepWithNext=True,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            fontName="SourceSans-Bold",
            fontSize=20,
            leading=23,
            textColor=NAVY,
            spaceBefore=0,
            spaceAfter=11,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            fontName="SourceSans-Semibold",
            fontSize=13.2,
            leading=16,
            textColor=TEAL,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            fontName="SourceSans-Semibold",
            fontSize=10.5,
            leading=13,
            textColor=NAVY,
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "toc_title": ParagraphStyle(
            "TOCTitle",
            fontName="SourceSans-Bold",
            fontSize=23,
            leading=27,
            textColor=NAVY,
            spaceAfter=13,
        ),
        "caption": ParagraphStyle(
            "Caption",
            fontName="SourceSans-Semibold",
            fontSize=TOKENS["caption"]["size_pt"],
            leading=TOKENS["caption"]["leading_pt"],
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=1,
        ),
        "source": ParagraphStyle(
            "Source",
            fontName="SourceSans",
            fontSize=6.8,
            leading=8.2,
            textColor=GREY,
            spaceAfter=6,
        ),
        "callout": ParagraphStyle(
            "Callout",
            fontName="SourceSerif-Semibold",
            fontSize=9.3,
            leading=12.4,
            textColor=NAVY,
            alignment=TA_LEFT,
        ),
        "table_title": ParagraphStyle(
            "TableTitle",
            fontName="SourceSans-Semibold",
            fontSize=9.2,
            leading=11,
            textColor=NAVY,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            fontName="SourceSans",
            fontSize=6.7,
            leading=8.0,
            textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "TableHead",
            fontName="SourceSans-Semibold",
            fontSize=6.8,
            leading=8.0,
            textColor=colors.white,
        ),
        "small": ParagraphStyle(
            "Small",
            fontName="SourceSans",
            fontSize=7.3,
            leading=9.3,
            textColor=INK,
            spaceAfter=2.6,
        ),
        "bib": ParagraphStyle(
            "Bibliography",
            fontName="SourceSerif",
            fontSize=8.0,
            leading=10.4,
            textColor=INK,
            leftIndent=7 * mm,
            firstLineIndent=-7 * mm,
            spaceAfter=4,
        ),
    }


def inline_markup(text: str) -> str:
    """Escape source text, then enable the small Markdown subset used here."""
    placeholders: dict[str, str] = {}

    def stash(pattern: str, template: str, value: str) -> str:
        def repl(match: re.Match[str]) -> str:
            key = f"@@M{len(placeholders)}@@"
            placeholders[key] = template.format(html.escape(match.group(1)))
            return key
        return re.sub(pattern, repl, value)

    text = stash(r"\*\*(.+?)\*\*", "<b>{}</b>", text)
    text = stash(r"(?<!\*)\*([^*]+?)\*(?!\*)", "<i>{}</i>", text)
    text = stash(r"`([^`]+?)`", '<font name="SourceSans">{}</font>', text)
    text = html.escape(text)
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text.replace("  ", " ")


def _tag(local: str, namespace: str) -> str:
    return f"{{{namespace}}}{local}"


def extract_author_letter(odt_path: Path) -> tuple[list[str], str]:
    """Return ReportLab-marked paragraphs and literal plain text from the ODT."""
    ns_text = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    ns_style = "urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    ns_fo = "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    with zipfile.ZipFile(odt_path) as zf:
        root = ET.fromstring(zf.read("content.xml"))

    italic_styles: set[str] = set()
    for style in root.findall(f".//{_tag('style', ns_style)}"):
        props = style.find(_tag("text-properties", ns_style))
        if props is not None and props.get(_tag("font-style", ns_fo)) == "italic":
            name = style.get(_tag("name", ns_style))
            if name:
                italic_styles.add(name)

    def node_content(node: ET.Element, marked: bool) -> str:
        out = html.escape(node.text or "") if marked else (node.text or "")
        for child in list(node):
            if child.tag == _tag("s", ns_text):
                count = int(child.get(_tag("c", ns_text), "1"))
                part = " " * count
            elif child.tag == _tag("line-break", ns_text):
                part = "\n"
            elif child.tag == _tag("tab", ns_text):
                part = "\t"
            else:
                part = node_content(child, marked)
                style_name = child.get(_tag("style-name", ns_text), "")
                if marked and style_name in italic_styles and part:
                    part = f"<i>{part}</i>"
            out += part
            out += html.escape(child.tail or "") if marked else (child.tail or "")
        return out

    marked_paragraphs: list[str] = []
    plain_paragraphs: list[str] = []
    for p in root.findall(f".//{_tag('p', ns_text)}"):
        marked = node_content(p, True).replace("\t", "    ")
        plain = node_content(p, False).replace("\t", "    ")
        marked_parts = re.split(r"\n{2,}", marked)
        plain_parts = re.split(r"\n{2,}", plain)
        for mpart, ppart in zip(marked_parts, plain_parts):
            mpart = mpart.strip("\n")
            ppart = ppart.strip("\n")
            if ppart.strip():
                marked_paragraphs.append(mpart.replace("\n", "<br/>"))
                plain_paragraphs.append(ppart)
    literal = "\n\n".join(plain_paragraphs).rstrip() + "\n"
    return marked_paragraphs, literal


class CoverPage(Flowable):
    def __init__(self) -> None:
        super().__init__()
        self.width = PAGE_W
        self.height = PAGE_H

    def wrap(self, avail_width: float, avail_height: float) -> tuple[float, float]:
        return avail_width, avail_height

    def draw(self) -> None:
        c = self.canv
        c.saveState()
        c.setFillColor(NAVY)
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

        # Abstract system: source nodes, a backbone and a load field.
        c.setStrokeColor(colors.Color(0.34, 0.73, 0.67, alpha=0.40))
        c.setLineWidth(1.3)
        paths = [
            [(22, 58), (49, 92), (41, 133), (73, 168), (62, 218), (98, 270)],
            [(31, 43), (64, 75), (89, 112), (113, 154), (146, 187), (178, 243)],
            [(76, 27), (103, 66), (134, 91), (154, 128), (185, 158), (197, 202)],
        ]
        for points in paths:
            p = c.beginPath()
            p.moveTo(points[0][0] * mm, points[0][1] * mm)
            for x, y in points[1:]:
                p.lineTo(x * mm, y * mm)
            c.drawPath(p, stroke=1, fill=0)

        for x, y, r, col in [
            (49, 92, 4.0, TEAL), (73, 168, 3.0, GOLD), (98, 270, 2.4, ORANGE),
            (89, 112, 5.0, MINT), (146, 187, 3.5, GOLD), (178, 243, 2.8, TEAL),
            (103, 66, 3.2, ORANGE), (154, 128, 4.4, TEAL), (185, 158, 2.4, GOLD),
        ]:
            c.setFillColor(col)
            c.circle(x * mm, y * mm, r * mm, stroke=0, fill=1)
            c.setStrokeColor(colors.white)
            c.setLineWidth(0.5)
            c.circle(x * mm, y * mm, (r + 1.8) * mm, stroke=1, fill=0)

        c.setFillColor(colors.Color(1, 1, 1, alpha=0.055))
        c.circle(188 * mm, 45 * mm, 58 * mm, stroke=0, fill=1)
        c.circle(188 * mm, 45 * mm, 40 * mm, stroke=0, fill=1)

        c.setFillColor(GOLD)
        c.rect(22 * mm, 220 * mm, 33 * mm, 1.5 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("SourceSans-Bold", 29)
        title_lines = ["Electricidad argentina:", "cambio, límites", "y decisiones"]
        y = 207 * mm
        for line in title_lines:
            c.drawString(22 * mm, y, line)
            y -= 12.2 * mm

        subtitle = Paragraph(
            html.escape(TOKENS["subtitle"]),
            ParagraphStyle(
                "CoverSubtitle",
                fontName="SourceSans",
                fontSize=12.5,
                leading=16,
                textColor=colors.HexColor("#DCE9E8"),
            ),
        )
        subtitle.wrapOn(c, 113 * mm, 42 * mm)
        subtitle.drawOn(c, 22 * mm, 144 * mm)

        c.setFillColor(colors.HexColor("#DCE9E8"))
        c.setFont("SourceSans-Semibold", 10.5)
        c.drawString(22 * mm, 28 * mm, TOKENS["author"])
        c.setFont("SourceSans", 8.5)
        c.drawString(22 * mm, 21 * mm, "v0.10.0 · revisión del autor · agosto de 2026")
        c.setFillColor(MINT)
        c.rect(22 * mm, 17 * mm, 166 * mm, 0.6 * mm, stroke=0, fill=1)
        c.restoreState()


class EmbeddedFontCanvas(Canvas):
    """Avoid ReportLab's otherwise unused, non-embedded Helvetica resource."""

    def __init__(self, *args, **kwargs) -> None:
        # BaseDocTemplate explicitly passes its Helvetica defaults, so this
        # must replace—not merely default—the initial graphics-state font.
        kwargs["initialFontName"] = "SourceSans"
        kwargs["initialFontSize"] = 9
        super().__init__(*args, **kwargs)


class ReportDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs) -> None:
        super().__init__(filename, pagesize=A4, **kwargs)
        cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        body_frame = Frame(LEFT, BOTTOM, BODY_W, BODY_H, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(
            [
                PageTemplate(id="cover", frames=[cover_frame], onPage=self._cover_page),
                PageTemplate(id="body", frames=[body_frame], onPage=self._body_metadata, onPageEnd=self._body_page),
            ]
        )

    def _metadata(self, canvas) -> None:
        canvas.setTitle(TOKENS["title"])
        canvas.setAuthor(TOKENS["author"])
        canvas.setSubject("Sistema eléctrico argentino 2005–2025; red 2026; transición y capacidades tecnológicas")
        canvas.setKeywords("Argentina, electricidad, CAMMESA, SADI, transición energética, red, renovables, hidráulica")
        canvas.setCreator("Paquete reproducible TGCP v0.10.0")

    def _cover_page(self, canvas, doc) -> None:
        self._metadata(canvas)

    def _body_metadata(self, canvas, doc) -> None:
        self._metadata(canvas)

    def _body_page(self, canvas, doc) -> None:
        canvas.saveState()
        physical = canvas.getPageNumber()
        if physical > 2:
            canvas.setStrokeColor(colors.HexColor("#C8D5D6"))
            canvas.setLineWidth(0.45)
            canvas.line(LEFT, PAGE_H - 14 * mm, PAGE_W - RIGHT, PAGE_H - 14 * mm)
            canvas.setFillColor(GREY)
            canvas.setFont("SourceSans-Semibold", 6.7)
            canvas.drawString(LEFT, PAGE_H - 11 * mm, "ELECTRICIDAD ARGENTINA · CAMBIO, LÍMITES Y DECISIONES")
            canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 11 * mm, "REVISIÓN DEL AUTOR")
        canvas.setStrokeColor(colors.HexColor("#C8D5D6"))
        canvas.setLineWidth(0.45)
        canvas.line(LEFT, 13.5 * mm, PAGE_W - RIGHT, 13.5 * mm)
        canvas.setFillColor(GREY)
        canvas.setFont("SourceSans", 7)
        canvas.drawString(LEFT, 9.5 * mm, "TGCP v0.10.0")
        canvas.drawRightString(PAGE_W - RIGHT, 9.5 * mm, str(max(1, physical - 1)))
        canvas.restoreState()

    def afterFlowable(self, flowable) -> None:
        if isinstance(flowable, Paragraph) and hasattr(flowable, "_toc_level"):
            level = flowable._toc_level
            text = flowable.getPlainText()
            key = flowable._bookmark_name
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=(level > 0))
            # The cover is unnumbered; displayed folios begin on the author letter.
            self.notify("TOCEntry", (level, text, max(1, self.page - 1), key))


def heading(text: str, level: int, style: ParagraphStyle, bookmark: str) -> Paragraph:
    p = Paragraph(inline_markup(text), style)
    p._toc_level = level
    p._bookmark_name = bookmark
    return p


def load_figure_register() -> dict[str, dict[str, str]]:
    with REGISTER_PATH.open(encoding="utf-8", newline="") as fh:
        return {row["figure_id"]: row for row in csv.DictReader(fh)}


def figure_flowables(fid: str, reg: dict[str, dict[str, str]], st: dict[str, ParagraphStyle]) -> list[Flowable]:
    row = reg[fid]
    path = ROOT / row["png"]
    with PILImage.open(path) as im:
        px_w, px_h = im.size
    max_w = BODY_W
    max_h = 181 * mm if row["map_flag"] == "YES" else 118 * mm
    scale = min(max_w / px_w, max_h / px_h)
    draw_w, draw_h = px_w * scale, px_h * scale
    img = Image(str(path), width=draw_w, height=draw_h)
    label = "Mapa" if row["map_flag"] == "YES" else "Figura"
    cap = Paragraph(f"<b>{label} {html.escape(fid)}.</b> {html.escape(row['title_es'])}.", st["caption"])
    src = Paragraph(f"Fuente: {html.escape(row['data_source'])}. Elaboración y límites: paquete v0.10.0.", st["source"])
    return [KeepTogether([img, cap, src])]


def table_flowables(tid: str, st: dict[str, ParagraphStyle]) -> list[Flowable]:
    spec = TABLES[tid]
    title = Paragraph(f"<b>Tabla {tid}.</b> {html.escape(spec['title'])}", st["table_title"])
    data: list[list[Paragraph]] = []
    data.append([Paragraph(html.escape(str(x)), st["table_head"]) for x in spec["columns"]])
    for row in spec["rows"]:
        data.append([Paragraph(inline_markup(str(x)), st["table_cell"]) for x in row])
    ncols = len(spec["columns"])
    # Slightly favor the first and last columns where explanatory text accumulates.
    if ncols == 4:
        widths = [BODY_W * 0.22, BODY_W * 0.25, BODY_W * 0.24, BODY_W * 0.29]
    elif ncols == 5:
        widths = [BODY_W * 0.26, BODY_W * 0.17, BODY_W * 0.19, BODY_W * 0.19, BODY_W * 0.19]
    elif ncols == 6:
        widths = [BODY_W * 0.17, BODY_W * 0.16, BODY_W * 0.16, BODY_W * 0.15, BODY_W * 0.18, BODY_W * 0.18]
    else:
        widths = [BODY_W / ncols] * ncols
    table = LongTable(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "SourceSans"),
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BCCBCC")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    note = Paragraph(html.escape(spec["note"]), st["source"])
    return [title, table, Spacer(1, 2), note]


def bibliography_flowables(st: dict[str, ParagraphStyle]) -> list[Flowable]:
    out: list[Flowable] = []
    for entry in BIBLIOGRAPHY:
        author = html.escape(entry["author"])
        year = html.escape(entry["year"])
        title = html.escape(entry["title"])
        kind = html.escape(entry["kind"])
        url = entry.get("url", "")
        linked_title = f'<link href="{html.escape(url)}" color="#188B86">{title}</link>' if url else title
        out.append(Paragraph(f"<b>{author} ({year}).</b> {linked_title}. {kind}.", st["bib"]))
    return out


def lists_flowables(reg: dict[str, dict[str, str]], st: dict[str, ParagraphStyle]) -> list[Flowable]:
    out: list[Flowable] = [Paragraph("Figuras", st["h2"])]
    for fid, row in reg.items():
        label = "Mapa" if row["map_flag"] == "YES" else "Figura"
        out.append(Paragraph(f"<b>{label} {html.escape(fid)}.</b> {html.escape(row['title_es'])}.", st["small"]))
    out.append(Paragraph("Tablas", st["h2"]))
    for tid, spec in TABLES.items():
        out.append(Paragraph(f"<b>Tabla {html.escape(tid)}.</b> {html.escape(spec['title'])}.", st["small"]))
    return out


def parse_narrative(st: dict[str, ParagraphStyle], reg: dict[str, dict[str, str]]) -> list[Flowable]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story: list[Flowable] = []
    bookmark_count = 0
    first_title_skipped = False

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line == "# Electricidad argentina: cambio, límites y decisiones" and not first_title_skipped:
            first_title_skipped = True
            continue

        m = re.fullmatch(r"\{\{FIG:([FM]\d{2})\}\}", line)
        if m:
            fid = m.group(1)
            if reg[fid]["map_flag"] == "YES":
                story.append(PageBreak())
            story.extend(figure_flowables(fid, reg, st))
            continue
        m = re.fullmatch(r"\{\{TABLE:(T\d{2})\}\}", line)
        if m:
            story.extend(table_flowables(m.group(1), st))
            continue
        if line == "{{BIBLIOGRAPHY}}":
            story.extend(bibliography_flowables(st))
            continue
        if line == "{{LISTS}}":
            story.extend(lists_flowables(reg, st))
            continue

        if line.startswith("# "):
            story.append(PageBreak())
            text = line[2:].strip()
            bookmark_count += 1
            story.append(heading(text, 0, st["h1"], f"h{bookmark_count:03d}"))
            continue
        if line.startswith("## "):
            text = line[3:].strip()
            if re.match(r"^\d+\.\s", text):
                story.append(PageBreak())
                level, style = 0, st["h1"]
            else:
                level, style = 1, st["h2"]
            bookmark_count += 1
            story.append(heading(text, level, style, f"h{bookmark_count:03d}"))
            continue
        if line.startswith("### "):
            text = line[4:].strip()
            bookmark_count += 1
            story.append(heading(text, 2, st["h3"], f"h{bookmark_count:03d}"))
            continue
        if line.startswith("> "):
            call = Table(
                [[Paragraph(inline_markup(line[2:].strip()), st["callout"])]],
                colWidths=[BODY_W],
                style=TableStyle(
                    [
                        ("FONTNAME", (0, 0), (-1, -1), "SourceSans"),
                        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                        ("BOX", (0, 0), (-1, -1), 0.7, TEAL),
                        ("LINEBEFORE", (0, 0), (0, -1), 4, TEAL),
                        ("LEFTPADDING", (0, 0), (-1, -1), 11),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                ),
            )
            story.extend([Spacer(1, 3), call, Spacer(1, 7)])
            continue
        story.append(Paragraph(inline_markup(line), st["body"]))
    return story


def make_toc(st: dict[str, ParagraphStyle]) -> TableOfContents:
    toc = TableOfContents(
        tableStyle=TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "SourceSans"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    toc.levelStyles = [
        ParagraphStyle(
            "TOCLevel1",
            fontName="SourceSans-Semibold",
            fontSize=9.1,
            leading=12,
            textColor=NAVY,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=4,
        ),
        ParagraphStyle(
            "TOCLevel2",
            fontName="SourceSans",
            fontSize=8.1,
            leading=10.3,
            textColor=INK,
            leftIndent=8 * mm,
            firstLineIndent=0,
            spaceBefore=1.2,
        ),
        ParagraphStyle(
            "TOCLevel3",
            fontName="SourceSans",
            fontSize=7.4,
            leading=9.2,
            textColor=GREY,
            leftIndent=15 * mm,
            firstLineIndent=0,
        ),
    ]
    toc.dotsMinLevel = 0
    return toc


def build(output: Path) -> None:
    register_fonts()
    st = styles()
    reg = load_figure_register()
    letter_marked, letter_literal = extract_author_letter(LETTER_ODT)
    extracted = ROOT / "editorial/source/CARTA_AUTOR_LITERAL_EXTRAIDA_v0.10.0.txt"
    extracted.write_text(letter_literal, encoding="utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    doc = ReportDocTemplate(
        str(output),
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title=TOKENS["title"],
        author=TOKENS["author"],
    )

    story: list[Flowable] = [
        CoverPage(),
        NextPageTemplate("body"),
        PageBreak(),
        Paragraph("Carta del autor:", st["letter_heading"]),
    ]
    for para in letter_marked:
        story.append(Paragraph(para, st["letter"]))
    story.extend(
        [
            PageBreak(),
            Paragraph("Índice", st["toc_title"]),
            make_toc(st),
        ]
    )
    story.extend(parse_narrative(st, reg))
    doc.multiBuild(story, maxPasses=6, canvasmaker=EmbeddedFontCanvas)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "reports/ELECTRICIDAD_ARGENTINA_v0.10.0_REVISION_AUTOR.pdf",
    )
    args = parser.parse_args()
    build(args.output.resolve())


if __name__ == "__main__":
    main()
