"""Convert Cold Email Setup markdown docs to PDF -- RIOA brand styling.

Brand aesthetic (per CLAUDE.md):
  - Type: Cormorant Garamond (headings) / Jost (body) -- warm editorial pair
  - Palette: charcoal (#1a1614) / cream (#f5ede0) / gold (#b08d57)
  - Tone: warm, editorial, premium

Downloads Google Fonts on first run (cached in ./fonts/). Falls back to
Helvetica/Times-Roman if download fails (no internet, etc).

Renderer features:
  - Headings keep with next so they don't orphan at page bottoms
  - Nested bullets detected via 3+ leading spaces; rendered with deeper
    indent and small dot marker for clear visual hierarchy
  - Fenced code blocks rendered as cream/gold-bordered Tables with
    wrapping Paragraphs (so paste-ready strings don't truncate)
  - Markdown tables: gold header band, warm border, cream alternating rows
"""
import re
import sys
import urllib.request
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle,
    PageBreak, CondPageBreak,
)


# ---------- Brand palette ----------
CHARCOAL_DEEP = HexColor("#1a1614")    # headings
CHARCOAL_BODY = HexColor("#2a2622")    # body text
CREAM_BG = HexColor("#f5ede0")         # code bg, table header bg
CREAM_LIGHT = HexColor("#faf6ef")      # subtle accents
GOLD = HexColor("#b08d57")             # accents, rules, borders
GOLD_LIGHT = HexColor("#d4b884")       # softer gold for borders
WARM_GRAY = HexColor("#8b7e6f")        # secondary text


# ---------- Font registration ----------
FONTS_DIR = Path(__file__).parent / "fonts"
FONTS_DIR.mkdir(exist_ok=True)

FONT_URLS = {
    # Google Fonts repo only ships variable fonts (CormorantGaramond[wght].ttf
    # and Jost[wght].ttf). When loaded by ReportLab, they render at the default
    # weight (Regular). For bold visual contrast we pair with Helvetica-Bold and
    # rely on size hierarchy + color for headings.
    "CormorantGaramond.ttf":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf",
    "CormorantGaramond-Italic.ttf":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond-Italic%5Bwght%5D.ttf",
    "Jost.ttf":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/jost/Jost%5Bwght%5D.ttf",
    "Jost-Italic.ttf":
        "https://raw.githubusercontent.com/google/fonts/main/ofl/jost/Jost-Italic%5Bwght%5D.ttf",
}


def _download_fonts():
    """Download Google Fonts to ./fonts/ if not already cached."""
    for filename, url in FONT_URLS.items():
        target = FONTS_DIR / filename
        if target.exists() and target.stat().st_size > 1000:
            continue
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, target)
        except Exception as e:
            print(f"  Failed: {e}")
            return False
    return True


def register_fonts():
    """Register Cormorant Garamond + Jost variable fonts.

    Variable fonts render at default weight only. For bold visual contrast,
    we pair with Helvetica-Bold (built-in) rather than trying to access the
    weight axis (which ReportLab doesn't support cleanly).

    Returns (heading_font, body_font) family names.
    Falls back to Times-Roman/Helvetica on download or registration failure.
    """
    if not _download_fonts():
        print("Font download failed. Using built-in fonts.")
        return ("Times-Roman", "Helvetica")
    try:
        pdfmetrics.registerFont(TTFont("CormorantGaramond",
                                       str(FONTS_DIR / "CormorantGaramond.ttf")))
        pdfmetrics.registerFont(TTFont("CormorantGaramond-Italic",
                                       str(FONTS_DIR / "CormorantGaramond-Italic.ttf")))
        pdfmetrics.registerFont(TTFont("Jost",
                                       str(FONTS_DIR / "Jost.ttf")))
        pdfmetrics.registerFont(TTFont("Jost-Italic",
                                       str(FONTS_DIR / "Jost-Italic.ttf")))
        # Pair brand serifs with Helvetica-Bold for inline bold (variable fonts
        # don't expose weight axes via ReportLab's TTFont interface).
        pdfmetrics.registerFontFamily(
            "Jost", normal="Jost", bold="Helvetica-Bold",
            italic="Jost-Italic", boldItalic="Helvetica-Bold",
        )
        pdfmetrics.registerFontFamily(
            "CormorantGaramond",
            normal="CormorantGaramond", bold="Helvetica-Bold",
            italic="CormorantGaramond-Italic", boldItalic="Helvetica-Bold",
        )
        print("Brand fonts registered: Cormorant Garamond + Jost")
        return ("CormorantGaramond", "Jost")
    except Exception as e:
        print(f"Font registration failed: {e}. Using built-in fonts.")
        return ("Times-Roman", "Helvetica")


HEADING_FONT, BODY_FONT = register_fonts()
# Use the brand serif for headings (Cormorant Garamond at large size reads as
# display weight even though it's the variable font's default ~400 weight).
HEADING_FACE = HEADING_FONT  # CormorantGaramond or Times-Roman fallback
H3_FACE = BODY_FONT          # Jost for H3 = different family creates hierarchy variety
BODY_BOLD = "Helvetica-Bold"  # for inline <b> in body (acceptable family mix)

# SCHABO Condensed = the display face for H1/H2 mastheads. Bold condensed sans
# (Tom Robin Karlsson, free for commercial use). Falls back to the brand serif
# if the file is missing. Converted OTF->TTF for ReportLab embedding.
SCHABO_PATH = FONTS_DIR / "SCHABO-Condensed.ttf"
HEADING_DISPLAY = HEADING_FACE
try:
    if SCHABO_PATH.exists() and SCHABO_PATH.stat().st_size > 1000:
        pdfmetrics.registerFont(TTFont("SCHABO", str(SCHABO_PATH)))
        HEADING_DISPLAY = "SCHABO"
        print("Display heading face registered: SCHABO Condensed")
    else:
        print("SCHABO not found; using Cormorant for headings.")
except Exception as e:
    print(f"SCHABO registration failed ({e}); using Cormorant for headings.")


# ---------- Paragraph styles ----------
styles = getSampleStyleSheet()

# Headings: SCHABO Condensed display face in charcoal for a bold, modern
# masthead. Hierarchy by size: large SCHABO (H1) -> medium SCHABO (H2) ->
# small gold Jost-bold kicker (H3) for contrast and readability at small size.
# Condensed faces read narrow, so H1/H2 are sized up vs the old serif scale.
H1 = ParagraphStyle(
    "H1", parent=styles["Heading1"],
    fontName=HEADING_DISPLAY, fontSize=40, leading=42,
    textColor=CHARCOAL_DEEP, spaceBefore=0, spaceAfter=13,
    keepWithNext=1,
)
H2 = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontName=HEADING_DISPLAY, fontSize=27, leading=30,
    textColor=CHARCOAL_DEEP, spaceBefore=22, spaceAfter=9,
    keepWithNext=1,
)
H3 = ParagraphStyle(
    "H3", parent=styles["Heading3"],
    fontName=BODY_BOLD, fontSize=11.5, leading=15,
    textColor=GOLD, spaceBefore=14, spaceAfter=4,
    keepWithNext=1,
)
BODY = ParagraphStyle(
    "Body", parent=styles["BodyText"],
    fontName=BODY_FONT, fontSize=10.5, leading=15.5,
    textColor=CHARCOAL_BODY, spaceAfter=8, alignment=TA_LEFT,
)
BULLET = ParagraphStyle(
    "Bullet", parent=BODY,
    leftIndent=18, firstLineIndent=-12, spaceAfter=4,
)
BULLET_NESTED = ParagraphStyle(
    "BulletNested", parent=BODY,
    leftIndent=46, firstLineIndent=-14, spaceAfter=3,
    fontSize=10.5, leading=15, textColor=CHARCOAL_BODY,
)
NUMBER = ParagraphStyle(
    "Number", parent=BODY,
    leftIndent=24, firstLineIndent=-20, spaceAfter=4,
)
CODE_PARA = ParagraphStyle(
    "CodePara", parent=BODY,
    fontName="Courier", fontSize=9.5, leading=13,
    textColor=CHARCOAL_DEEP,
    leftIndent=0, rightIndent=0, spaceAfter=0,
)
CALLOUT_PARA = ParagraphStyle(
    "CalloutPara", parent=BODY,
    fontName=BODY_FONT, fontSize=10.5, leading=15.5,
    textColor=CHARCOAL_DEEP,
    leftIndent=0, rightIndent=0, spaceAfter=4,
)
CALLOUT_LABEL = ParagraphStyle(
    "CalloutLabel", parent=BODY,
    fontName=BODY_BOLD, fontSize=9, leading=12,
    textColor=GOLD,
    leftIndent=0, rightIndent=0, spaceAfter=6,
)


# ---------- Helpers ----------
def escape_xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline_md_to_rl(text: str) -> str:
    """Turn **bold** / *italic* / `code` / [text](url) into ReportLab inline markup."""
    # Extract markdown links BEFORE escaping XML, so the URL doesn't get mangled.
    # Replace each [text](url) with a placeholder, store the link, restore after escaping.
    link_placeholders = []
    def _stash_link(m):
        link_text, url = m.group(1), m.group(2)
        idx = len(link_placeholders)
        link_placeholders.append((link_text, url))
        return f"\x00LINK{idx}\x00"
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _stash_link, text)

    text = escape_xml(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(
        r"`([^`]+?)`",
        r'<font name="Courier" size="9.5" color="#3a3530">\1</font>',
        text,
    )

    # Restore links as ReportLab <link> tags. Gold-coloured + underlined to read as hyperlinks.
    for idx, (link_text, url) in enumerate(link_placeholders):
        # Re-process the link text for inline formatting (bold/italic inside link text)
        inner = escape_xml(link_text)
        inner = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", inner)
        inner = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)", r"<i>\1</i>", inner)
        safe_url = url.replace('"', "&quot;").replace("&", "&amp;")
        replacement = (
            f'<link href="{safe_url}" color="#b08d57">'
            f'<u>{inner}</u></link>'
        )
        text = text.replace(f"\x00LINK{idx}\x00", replacement)

    return text


def prose_callout_flowable(text: str):
    """Render a `>` blockquote as a cream/gold-bordered callout using body font.

    If the first line is ALL CAPS (and short), render it as a gold label above
    the body content. Otherwise render the whole block as prose paragraphs.
    """
    lines = [ln.rstrip() for ln in text.split("\n")]
    # Drop empty leading/trailing lines
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()

    paragraphs = []
    if lines and lines[0].strip() and lines[0].strip().isupper() and len(lines[0]) <= 60:
        paragraphs.append(Paragraph(escape_xml(lines[0].strip()), CALLOUT_LABEL))
        lines = lines[1:]
        # Skip a leading blank after the label
        while lines and lines[0].strip() == "":
            lines.pop(0)

    # Group remaining lines into paragraphs (blank line = paragraph break)
    buf = []
    for ln in lines:
        if ln.strip() == "":
            if buf:
                paragraphs.append(Paragraph(inline_md_to_rl(" ".join(buf)), CALLOUT_PARA))
                buf = []
        else:
            buf.append(ln.strip())
    if buf:
        paragraphs.append(Paragraph(inline_md_to_rl(" ".join(buf)), CALLOUT_PARA))

    tbl = Table(
        [[paragraphs]],
        colWidths=["*"],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CREAM_BG),
            ("LINEABOVE", (0, 0), (-1, -1), 1.5, GOLD),
            ("LINEBELOW", (0, 0), (-1, -1), 1.5, GOLD),
            ("LINEBEFORE", (0, 0), (-1, -1), 1.5, GOLD),
            ("LINEAFTER", (0, 0), (-1, -1), 1.5, GOLD),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]),
    )
    return tbl


def code_block_flowable(code_text: str):
    lines = code_text.split("\n")
    paragraphs = []
    for line in lines:
        if line.strip() == "":
            paragraphs.append(Spacer(1, 6))
        else:
            leading = len(line) - len(line.lstrip(" "))
            content = "&nbsp;" * leading + escape_xml(line.lstrip(" "))
            paragraphs.append(Paragraph(content, CODE_PARA))

    tbl = Table(
        [[paragraphs]],
        colWidths=["*"],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CREAM_BG),
            ("LINEABOVE", (0, 0), (-1, -1), 1.5, GOLD),
            ("LINEBELOW", (0, 0), (-1, -1), 1.5, GOLD),
            ("LINEBEFORE", (0, 0), (-1, -1), 1.5, GOLD),
            ("LINEAFTER", (0, 0), (-1, -1), 1.5, GOLD),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]),
    )
    return tbl


TABLE_HEADER = ParagraphStyle(
    "TableHeader", parent=BODY,
    fontName=BODY_BOLD, fontSize=10, leading=13,
    textColor=CHARCOAL_DEEP, spaceAfter=0,
)
TABLE_CELL = ParagraphStyle(
    "TableCell", parent=BODY,
    fontSize=10, leading=13.5, spaceAfter=0,
    textColor=CHARCOAL_BODY,
)


def parse_markdown_table(lines, start_i):
    if start_i + 1 >= len(lines):
        return None, start_i
    header = lines[start_i].rstrip()
    sep = lines[start_i + 1].rstrip()
    if not header.lstrip().startswith("|"):
        return None, start_i
    if not re.match(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$", sep):
        return None, start_i

    def split_row(row):
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [c.strip() for c in row.split("|")]

    headers = split_row(header)
    ncols = len(headers)
    rows = []
    i = start_i + 2
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        cells = split_row(lines[i].rstrip())
        cells = (cells + [""] * ncols)[:ncols]
        rows.append(cells)
        i += 1

    data = [[Paragraph(inline_md_to_rl(h), TABLE_HEADER) for h in headers]]
    for r in rows:
        data.append([Paragraph(inline_md_to_rl(c), TABLE_CELL) for c in r])

    tbl = Table(data, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), CREAM_BG),
        ("LINEBELOW", (0, 0), (-1, 0), 1.2, GOLD),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, GOLD_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.6, GOLD_LIGHT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    # Subtle alternating row backgrounds for editorial feel
    for r_idx in range(2, len(data), 2):
        style_cmds.append(("BACKGROUND", (0, r_idx), (-1, r_idx), CREAM_LIGHT))
    tbl.setStyle(TableStyle(style_cmds))
    return tbl, i


def md_to_flowables(md_text: str):
    flows = []
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        if stripped.lstrip().startswith("|"):
            tbl, next_i = parse_markdown_table(lines, i)
            if tbl is not None:
                flows.append(tbl)
                flows.append(Spacer(1, 8))
                i = next_i
                continue

        if re.match(r"^\s*---+\s*$", stripped):
            flows.append(Spacer(1, 6))
            flows.append(HRFlowable(width="100%", thickness=0.8,
                                    color=GOLD,
                                    spaceBefore=2, spaceAfter=12))
            i += 1
            continue

        if stripped.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].rstrip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            flows.append(code_block_flowable("\n".join(buf)))
            flows.append(Spacer(1, 8))
            continue

        # Markdown blockquote -> styled prose callout (cream/gold box, body font)
        if stripped.lstrip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                line_content = lines[i].lstrip()
                if line_content.startswith("> "):
                    buf.append(line_content[2:])
                elif line_content.startswith(">"):
                    buf.append(line_content[1:])
                else:
                    buf.append(line_content)
                i += 1
            flows.append(prose_callout_flowable("\n".join(buf)))
            flows.append(Spacer(1, 10))
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            content = inline_md_to_rl(m.group(2))
            if level == 1:
                flows.append(Paragraph(content, H1))
            elif level == 2:
                # Each H2 (section) starts on a new page in the common case --
                # but use CondPageBreak so we don't leave a near-empty page
                # when a previous section's trailing paragraph orphans onto a
                # fresh page. CondPageBreak(N) only advances if remaining
                # vertical space is less than N. With N=400pt (~half a page),
                # if the current page is mostly empty (orphan-only case),
                # remaining > 400, no break -- H2 continues on same page.
                # If the current page is mostly full, remaining < 400, break
                # fires and H2 starts fresh.
                # Skip even the conditional break if H2 is literally the first
                # flowable (avoids a blank cover when a doc has no H1).
                if flows:
                    flows.append(CondPageBreak(400))
                flows.append(Paragraph(content, H2))
            else:
                flows.append(Paragraph(content, H3))
            i += 1
            continue

        if re.match(r"^\s*[-]\s+", stripped) and not re.match(r"^\s*---", stripped):
            while i < len(lines) and re.match(r"^\s*[-]\s+", lines[i].rstrip()) \
                    and not re.match(r"^\s*---", lines[i].rstrip()):
                raw_line = lines[i].rstrip()
                indent_len = len(raw_line) - len(raw_line.lstrip(" \t"))
                if indent_len >= 3:
                    style = BULLET_NESTED
                    # Nested marker: gold angle quote (›). Universally
                    # available glyph that renders in both Jost and Helvetica.
                    marker = '<font name="Helvetica" color="#b08d57">›</font>&nbsp;&nbsp;'
                else:
                    style = BULLET
                    # Top-level marker: gold filled bullet.
                    marker = '<font name="Helvetica" color="#b08d57">•</font>&nbsp;&nbsp;'
                item_text = re.sub(r"^\s*[-]\s+", "", raw_line)
                flows.append(Paragraph(marker + inline_md_to_rl(item_text), style))
                i += 1
            flows.append(Spacer(1, 4))
            continue

        if re.match(r"^\s*\d+\.\s+", stripped):
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i].rstrip()):
                m = re.match(r"^\s*(\d+)\.\s+(.*)$", lines[i].rstrip())
                num, item_text = m.group(1), m.group(2)
                flows.append(Paragraph(
                    f'<font name="Helvetica-Bold" color="#b08d57">{num}.</font>&nbsp;&nbsp;'
                    + inline_md_to_rl(item_text), NUMBER))
                i += 1
            flows.append(Spacer(1, 4))
            continue

        if stripped == "":
            i += 1
            continue

        buf = [stripped]
        i += 1
        while (i < len(lines)
               and lines[i].strip() != ""
               and not re.match(r"^(#{1,6}\s|[-]\s|\d+\.\s|```|---+)",
                                lines[i].lstrip())):
            buf.append(lines[i].rstrip())
            i += 1
        para = " ".join(buf)
        flows.append(Paragraph(inline_md_to_rl(para), BODY))

    return flows


def make_first_page_cover(title: str, classification: str = "Client Confidential",
                          eyebrow: str = "MARKET INTELLIGENCE  |  SECTOR REPORT"):
    """Draw a magazine-style cover treatment on page 1: charcoal banner across
    the top with RIOA logo + eyebrow line, gold accent rule below the banner,
    and the same footer used on inner pages. The H1/subtitle/metadata flow
    from markdown still renders below the banner (push them down with a Spacer
    inserted at the start of the flow stream)."""

    def draw(canvas, doc):
        canvas.saveState()
        width, height = A4

        # ---- Charcoal banner across top ~8cm ----
        banner_h = 8 * cm
        canvas.setFillColor(CHARCOAL_DEEP)
        canvas.rect(0, height - banner_h, width, banner_h, fill=1, stroke=0)

        # Logo treatment top-left: "RIOA" white-bold, "CONSULTING" gold below
        canvas.setFillColor(HexColor("#ffffff"))
        canvas.setFont(BODY_BOLD, 18)
        canvas.drawString(2.4 * cm, height - 2.2 * cm, "RIOA")
        canvas.setFillColor(GOLD)
        canvas.setFont(BODY_BOLD, 8.5)
        canvas.drawString(2.4 * cm, height - 2.75 * cm, "CONSULTING")

        # Eyebrow top-right
        canvas.setFillColor(HexColor("#ffffff"))
        canvas.setFont(BODY_FONT, 8.5)
        canvas.drawRightString(width - 2.4 * cm, height - 2.45 * cm, eyebrow)

        # Brand tagline at the BOTTOM of the banner area, left
        canvas.setFillColor(HexColor("#9c8b75"))
        canvas.setFont(BODY_FONT, 8)
        canvas.drawString(2.4 * cm, height - banner_h + 0.6 * cm,
                          "Strategy. Insight. Execution.")
        canvas.drawRightString(width - 2.4 * cm, height - banner_h + 0.6 * cm,
                               "rioaconsulting.com")

        # Short gold accent rule just below the banner
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(2.2)
        canvas.line(2.4 * cm, height - banner_h - 0.6 * cm,
                    6.5 * cm, height - banner_h - 0.6 * cm)

        # ---- Footer (same treatment as inner pages, so every page is signed) ----
        canvas.setStrokeColor(GOLD_LIGHT)
        canvas.setLineWidth(0.4)
        canvas.line(2.4 * cm, 1.75 * cm, width - 2.4 * cm, 1.75 * cm)
        canvas.setFont(BODY_FONT, 8.5)
        canvas.setFillColor(WARM_GRAY)
        canvas.drawString(2.4 * cm, 1.4 * cm, classification)
        canvas.drawRightString(width - 2.4 * cm, 1.4 * cm, f"Page {doc.page}")

        canvas.restoreState()

    return draw


def make_header_footer(title: str, classification: str = "Client Confidential"):
    """Create a draw function that paints a running header and footer on
    every page. Called by SimpleDocTemplate via onFirstPage / onLaterPages."""
    # Truncate long titles so they fit on the right side of the header
    short_title = title if len(title) <= 65 else title[:62] + "..."

    def draw(canvas, doc):
        canvas.saveState()
        width, height = A4

        # ---- Header ----
        canvas.setFont(BODY_BOLD, 8.5)
        canvas.setFillColor(GOLD)
        canvas.drawString(2.4 * cm, height - 1.5 * cm, "RIOA CONSULTING")
        canvas.setFont(BODY_FONT, 8.5)
        canvas.setFillColor(WARM_GRAY)
        canvas.drawRightString(width - 2.4 * cm, height - 1.5 * cm, short_title)
        canvas.setStrokeColor(GOLD_LIGHT)
        canvas.setLineWidth(0.4)
        canvas.line(2.4 * cm, height - 1.75 * cm, width - 2.4 * cm, height - 1.75 * cm)

        # ---- Footer ----
        canvas.setStrokeColor(GOLD_LIGHT)
        canvas.line(2.4 * cm, 1.75 * cm, width - 2.4 * cm, 1.75 * cm)
        canvas.setFont(BODY_FONT, 8.5)
        canvas.setFillColor(WARM_GRAY)
        canvas.drawString(2.4 * cm, 1.4 * cm, classification)
        canvas.drawRightString(width - 2.4 * cm, 1.4 * cm, f"Page {doc.page}")

        canvas.restoreState()

    return draw


def convert(md_path: Path, pdf_path: Path, title: str,
            classification: str = "Client Confidential",
            eyebrow: str = "MARKET INTELLIGENCE  |  SECTOR REPORT"):
    text = md_path.read_text(encoding="utf-8")
    flows = md_to_flowables(text)
    # Push the first content (H1, subtitle, metadata) down past the cover
    # banner drawn by make_first_page_cover. The banner is 8cm; topMargin is
    # 2.5cm; so we need ~5.5cm of extra spacer to clear the banner cleanly.
    flows.insert(0, Spacer(1, 5.8 * cm))
    doc = SimpleDocTemplate(
        str(pdf_path), pagesize=A4,
        title=title, author="RIOA Consulting",
        leftMargin=2.4*cm, rightMargin=2.4*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
    )
    cover = make_first_page_cover(title, classification, eyebrow)
    hf = make_header_footer(title, classification)
    doc.build(flows, onFirstPage=cover, onLaterPages=hf)
    print(f"Wrote: {pdf_path}")


if __name__ == "__main__":
    # CLI usage:
    #   python _md_to_pdf.py <input.md> [output.pdf] ["Title"] ["Classification"]
    #
    # All args after the input path are optional. Defaults:
    #   output.pdf      -> input.md with .pdf extension
    #   Title           -> derived from filename
    #   Classification  -> "Client Confidential" (footer left)
    if len(sys.argv) < 2:
        print('Usage: python _md_to_pdf.py <input.md> [output.pdf] ["Title"] ["Classification"]')
        sys.exit(1)
    md_path = Path(sys.argv[1]).resolve()
    if not md_path.exists():
        print(f"Error: markdown file not found: {md_path}")
        sys.exit(1)
    pdf_path = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else md_path.with_suffix(".pdf")
    title = sys.argv[3] if len(sys.argv) >= 4 else md_path.stem.replace("_", " ").replace("-", " ")
    classification = sys.argv[4] if len(sys.argv) >= 5 else "Client Confidential"
    eyebrow = sys.argv[5] if len(sys.argv) >= 6 else "MARKET INTELLIGENCE  |  SECTOR REPORT"
    convert(md_path, pdf_path, title, classification, eyebrow)
