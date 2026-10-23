"""RIOA PDF -- SITE theme (default since 2026-10-13).

Matches the live rioaconsulting.com design, read from its CSS on 2026-10-13:
  - Field #080807, panel #10100e, edge #29261f
  - Text #f4f0e6, cream #f0e8d9, muted #a39e92, gold accent #b89452
  - Type: Instrument Sans (headings 500, body 400, bold 600) with Cormorant
    Garamond italic for emphasis, Space Mono for code/ledger labels.
Fonts ship in ./fonts (Instrument Sans + Cormorant italic converted from the
site's own woff2 files, OFL licences alongside). Built from the Night Ledger
renderer (TOC, SOP cards, callouts, tables) with the site palette and cover.
"""
import re
import sys
import urllib.request
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle,
    PageBreak, CondPageBreak, Image as RLImage, KeepTogether,
)
from reportlab.lib.utils import ImageReader


# ---------- Brand palette ----------
CHARCOAL_DEEP = HexColor("#f4f0e6")    # headings
CHARCOAL_BODY = HexColor("#f4f0e6")    # body text
CREAM_BG = HexColor("#10100e")         # code bg, table header bg
CREAM_LIGHT = HexColor("#15120d")      # subtle accents
GOLD = HexColor("#b89452")             # accents, rules, borders
GOLD_LIGHT = HexColor("#29261f")       # softer gold for borders
WARM_GRAY = HexColor("#a39e92")        # secondary text


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
# --- SITE stack (matches rioaconsulting.com): Instrument Sans + Cormorant italic + Space Mono ---
SITE_ITALIC = "CormorantItalicSite"
try:
    pdfmetrics.registerFont(TTFont("InstrumentSans", str(FONTS_DIR / "InstrumentSans-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("InstrumentSans-Medium", str(FONTS_DIR / "InstrumentSans-Medium.ttf")))
    pdfmetrics.registerFont(TTFont("InstrumentSans-SemiBold", str(FONTS_DIR / "InstrumentSans-SemiBold.ttf")))
    pdfmetrics.registerFont(TTFont(SITE_ITALIC, str(FONTS_DIR / "CormorantGaramond-Italic-Site.ttf")))
    pdfmetrics.registerFont(TTFont("SpaceMono", str(FONTS_DIR / "SpaceMono-Regular.ttf")))
    pdfmetrics.registerFontFamily("SpaceMono", normal="SpaceMono",
        bold="SpaceMono", italic="SpaceMono", boldItalic="SpaceMono")
    pdfmetrics.registerFontFamily("InstrumentSans", normal="InstrumentSans",
        bold="InstrumentSans-SemiBold", italic=SITE_ITALIC, boldItalic="InstrumentSans-SemiBold")
    BODY_FONT = "InstrumentSans"
    LEDGER_MONO = "SpaceMono"
    print("Site stack registered: Instrument Sans / Cormorant italic / Space Mono")
except Exception as e:
    LEDGER_MONO = "Courier"
    print(f"site stack registration failed ({e}); falling back")
# Use the brand serif for headings (Cormorant Garamond at large size reads as
# display weight even though it's the variable font's default ~400 weight).
HEADING_FACE = HEADING_FONT  # CormorantGaramond or Times-Roman fallback
H3_FACE = BODY_FONT          # Jost for H3 = different family creates hierarchy variety
BODY_BOLD = "InstrumentSans-SemiBold" if BODY_FONT == "InstrumentSans" else "Helvetica-Bold"

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

try:
    pdfmetrics.getFont("InstrumentSans-Medium"); HEADING_DISPLAY = "InstrumentSans-Medium"
except Exception:
    pass
# Headings: SCHABO Condensed display face in charcoal for a bold, modern
# masthead. Hierarchy by size: large SCHABO (H1) -> medium SCHABO (H2) ->
# small gold Jost-bold kicker (H3) for contrast and readability at small size.
# Condensed faces read narrow, so H1/H2 are sized up vs the old serif scale.
H1 = ParagraphStyle(
    "H1", parent=styles["Heading1"],
    fontName=HEADING_DISPLAY, fontSize=30, leading=35,
    textColor=CHARCOAL_DEEP, spaceBefore=0, spaceAfter=13,
    keepWithNext=1,
)
H2 = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontName=HEADING_DISPLAY, fontSize=20, leading=25,
    textColor=CHARCOAL_DEEP, spaceBefore=22, spaceAfter=9,
    keepWithNext=1,
)
H3 = ParagraphStyle(
    "H3", parent=styles["Heading3"],
    fontName=BODY_BOLD, fontSize=11.5, leading=15,
    textColor=GOLD, spaceBefore=14, spaceAfter=4,
    keepWithNext=1,
)
# Table-of-contents entry styles.
TOC_TITLE = ParagraphStyle("TOCTitle", parent=H1, spaceAfter=18)
TOC_PART = ParagraphStyle(
    "TOCPart", fontName=HEADING_DISPLAY, fontSize=13, leading=20,
    textColor=GOLD, spaceBefore=13, spaceAfter=2,
)
TOC_PART_PAGE = ParagraphStyle(
    "TOCPartPage", parent=TOC_PART, alignment=TA_RIGHT,
)
TOC_MOD = ParagraphStyle(
    "TOCMod", fontName=BODY_FONT, fontSize=10.5, leading=17,
    textColor=CHARCOAL_BODY, leftIndent=14, spaceAfter=0,
)
TOC_MOD_PAGE = ParagraphStyle(
    "TOCModPage", parent=TOC_MOD, leftIndent=0, alignment=TA_RIGHT,
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
    fontName=LEDGER_MONO, fontSize=9.5, leading=13,
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

# ---------- SOP field-card styles (the terse "do-this-now" reference cards) ----------
# A blood-red left spine (the brand's one red wound) makes these unmistakable
# next to the gold script-callout boxes. Title in the emphasis red; steps reuse
# the normal numbered-list styling; source tag in small ledger mono.
SOP_WOUND = HexColor("#b89452")   # deep wound red for the structural left rule
SOP_TITLE = ParagraphStyle(
    "SOPTitle", parent=BODY,
    fontName=BODY_BOLD, fontSize=11.5, leading=14,
    textColor=HexColor("#b89452"), spaceBefore=0, spaceAfter=3,
)
SOP_USEWHEN = ParagraphStyle(
    "SOPUseWhen", parent=BODY,
    fontName=BODY_FONT, fontSize=9.5, leading=13,
    textColor=WARM_GRAY, spaceAfter=8,
)
SOP_SOURCE = ParagraphStyle(
    "SOPSource", parent=BODY,
    fontName=LEDGER_MONO, fontSize=7.5, leading=11,
    textColor=WARM_GRAY, spaceBefore=8, spaceAfter=0,
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
    # Bold = emphasis: render bold AND in the brand blood red so the important
    # lines pop off the bone body text (Vik, 2026-07-13).
    text = re.sub(r"\*\*(.+?)\*\*", r'<b><font color="#b89452">\1</font></b>', text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(
        r"`([^`]+?)`",
        r'<font name="SpaceMono" size="9.5" color="#b89452">\1</font>',
        text,
    )

    # Restore links as ReportLab <link> tags. Gold-coloured + underlined to read as hyperlinks.
    for idx, (link_text, url) in enumerate(link_placeholders):
        # Re-process the link text for inline formatting (bold/italic inside link text)
        inner = escape_xml(link_text)
        inner = re.sub(r"\*\*(.+?)\*\*", r'<b><font color="#b89452">\1</font></b>', inner)
        inner = re.sub(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)", r"<i>\1</i>", inner)
        safe_url = url.replace('"', "&quot;").replace("&", "&amp;")
        replacement = (
            f'<link href="{safe_url}" color="#b89452">'
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


def sop_card_flowable(inner_text: str):
    """Render a ```sop ... ``` block as a terse 'field card': a blood-red left
    spine, a red title, an optional 'Use when:' trigger, numbered steps (via the
    normal markdown pipeline), and an optional small mono `source:` tag. Visually
    distinct from the gold script-callout boxes so a reader can flip to it."""
    raw = inner_text.split("\n")
    while raw and raw[0].strip() == "":
        raw.pop(0)
    while raw and raw[-1].strip() == "":
        raw.pop()
    if not raw:
        return Spacer(1, 0)

    # Title = first non-empty line, minus any leading ### / marker glyph.
    title = raw[0].strip()
    title = re.sub(r"^#+\s*", "", title)
    title = re.sub(r"^[▸\-\*•]\s*", "", title)
    body_lines = raw[1:]

    use_when = None
    source = None
    kept = []
    for ln in body_lines:
        s = ln.strip()
        if use_when is None and re.match(r"(?i)^use when\s*[:\-·]", s):
            use_when = re.sub(r"(?i)^use when\s*[:\-·]\s*", "", s)
        elif re.match(r"(?i)^source\s*[:\-·]", s):
            source = re.sub(r"(?i)^source\s*[:\-·]\s*", "", s)
        else:
            kept.append(ln)

    cell = [Paragraph(inline_md_to_rl(title), SOP_TITLE)]
    if use_when:
        cell.append(Paragraph(
            '<font name="%s">Use when:</font> ' % BODY_BOLD + inline_md_to_rl(use_when),
            SOP_USEWHEN))
    body_md = "\n".join(kept).strip()
    if body_md:
        cell.extend(md_to_flowables(body_md))
    if source:
        cell.append(Paragraph("source · " + escape_xml(source), SOP_SOURCE))

    tbl = Table(
        [[cell]],
        colWidths=["*"],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CREAM_LIGHT),
            ("LINEBEFORE", (0, 0), (-1, -1), 3, SOP_WOUND),   # the red spine
            ("LINEABOVE", (0, 0), (-1, -1), 0.6, GOLD_LIGHT),
            ("LINEBELOW", (0, 0), (-1, -1), 0.6, GOLD_LIGHT),
            ("LINEAFTER", (0, 0), (-1, -1), 0.6, GOLD_LIGHT),
            ("LEFTPADDING", (0, 0), (-1, -1), 15),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]),
    )
    # Short cards never split (avoids an orphaned title at a page bottom); only
    # genuinely long ones stay splittable.
    return KeepTogether(tbl)


def code_block_flowable(code_text: str):
    # One Paragraph PER LINE, each its own table ROW, so long code blocks
    # SPLIT across pages instead of overflowing a single non-splitting cell.
    lines = code_text.split("\n")
    rows = []
    for line in lines:
        if line.strip() == "":
            rows.append([Paragraph("&nbsp;", CODE_PARA)])
        else:
            leading = len(line) - len(line.lstrip(" "))
            content = "&nbsp;" * leading + escape_xml(line.lstrip(" "))
            rows.append([Paragraph(content, CODE_PARA)])
    if not rows:
        rows = [[Paragraph("&nbsp;", CODE_PARA)]]

    n = len(rows)
    tbl = Table(
        rows,
        colWidths=["*"],
        splitByRow=1,
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CREAM_BG),
            # continuous side rails; top/bottom rails only on the outer edges
            ("LINEBEFORE", (0, 0), (-1, -1), 1.5, GOLD),
            ("LINEAFTER", (0, 0), (-1, -1), 1.5, GOLD),
            ("LINEABOVE", (0, 0), (-1, 0), 1.5, GOLD),
            ("LINEBELOW", (0, n - 1), (-1, n - 1), 1.5, GOLD),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            # frame breathing room only at the very top and very bottom line
            ("TOPPADDING", (0, 0), (-1, 0), 10),
            ("TOPPADDING", (0, 1), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, n - 2 if n > 1 else 0), 1),
            ("BOTTOMPADDING", (0, n - 1), (-1, n - 1), 10),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]),
    )
    # Blocks that FIT on one page never split (the ugly heading-plus-one-row
    # orphan at a page bottom). Only genuinely page-plus blocks stay splittable.
    est_h = n * (CODE_PARA.leading + 2) + 24
    if est_h < 560:
        return KeepTogether(tbl)
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


IMG_CAPTION = ParagraphStyle(
    "ImgCaption", parent=BODY,
    fontName=LEDGER_MONO, fontSize=8.5, leading=12,
    textColor=CHARCOAL_DEEP, spaceAfter=0,
)


def image_flowable(src: str, caption: str = ""):
    """![caption](path) -> framed screenshot + gold mono caption, kept together."""
    ir = ImageReader(src)
    iw, ih = ir.getSize()
    max_w = 440.0
    w = min(max_w, float(iw))
    h = float(ih) * (w / float(iw))
    # Never let a tall image overflow the page frame: cap height and re-derive
    # width so aspect is preserved (a very tall diagram becomes a centered strip
    # rather than raising a LayoutError).
    max_h = 610.0
    if h > max_h:
        h = max_h
        w = float(iw) * (h / float(ih))
    img = RLImage(src, width=w, height=h)
    inner = [[img]]
    frame = Table(inner, colWidths=[w + 8])
    frame.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, CHARCOAL_DEEP),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    items = [Spacer(1, 6), frame]
    if caption:
        items.append(Spacer(1, 4))
        items.append(Paragraph(escape_xml(caption), IMG_CAPTION))
    items.append(Spacer(1, 12))
    return KeepTogether(items)


def md_to_flowables(md_text: str):
    flows = []
    prev_was_part = False
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        m_img = re.match(r"^\s*!\[(.*?)\]\((.+?)\)\s*$", stripped)
        if m_img:
            cap, src = m_img.group(1), m_img.group(2)
            try:
                flows.append(image_flowable(src, cap))
            except Exception as ex:
                flows.append(Paragraph(escape_xml(f"[screenshot missing: {src}]"), IMG_CAPTION))
            i += 1
            continue

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

        # SOP field card: ```sop ... ``` (must be checked before the generic fence)
        if stripped.startswith("```sop"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].rstrip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # consume the closing fence
            flows.append(Spacer(1, 4))
            flows.append(sop_card_flowable("\n".join(buf)))
            flows.append(Spacer(1, 12))
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
                # A big H1 "PART X" / "APPENDIX" divider starts on a fresh page
                # (keeping its large look); the module H2 that follows sits on that
                # same page via the CondPageBreak below. The book title is the very
                # first flowable, so it never breaks.
                is_divider = bool(re.match(r"(?i)^(part|appendix)\b", m.group(2).strip()))
                if is_divider and flows:
                    flows.append(PageBreak())
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
                is_part = bool(re.match(r"(?i)^part\b", m.group(2).strip()))
                if flows:
                    # A "PART X" divider hard-breaks to a fresh page; the module
                    # that follows it sits on that SAME page (so the part opener
                    # is not a near-empty page). Ordinary section H2s use a
                    # conditional break so a trailing orphan doesn't strand a
                    # near-empty page.
                    if is_part:
                        flows.append(PageBreak())
                    else:
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
                    marker = '<font name="Helvetica" color="#b89452">›</font>&nbsp;&nbsp;'
                else:
                    style = BULLET
                    # Top-level marker: gold filled bullet.
                    marker = '<font name="Helvetica" color="#b89452">•</font>&nbsp;&nbsp;'
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
                    f'<font name="Helvetica-Bold" color="#b89452">{num}.</font>&nbsp;&nbsp;'
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
                          eyebrow: str = "Websites for U.S. local businesses", chapter: str = "00"):
    """SITE cover: the rioaconsulting.com hero on paper. Near-black field, a soft
    gold aura, RIOA wordmark with gold dot, a pill eyebrow, a large Instrument
    Sans title with an optional Cormorant italic subtitle (" -- " splits them),
    and a hairline ledger footer. Content starts on page 2."""
    FIELD = HexColor("#080807"); TEXT = HexColor("#f4f0e6"); MUTED = HexColor("#a39e92")
    EDGE = HexColor("#29261f"); GOLDC = HexColor("#b89452"); AURA = HexColor("#a87026")

    def draw(canvas, doc):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        canvas.saveState()
        W, H = A4
        canvas.setFillColor(FIELD); canvas.rect(0, 0, W, H, fill=1, stroke=0)
        # soft aura (stacked low-alpha discs), echoing the site's --aura glow
        canvas.setFillColor(AURA)
        for i in range(26):  # many faint discs = smooth falloff, no banding
            canvas.setFillAlpha(0.02)
            canvas.circle(W * 0.80, H * 0.30, 290 - i * 10, fill=1, stroke=0)
        canvas.setFillAlpha(1)
        # wordmark: RIOA + gold dot
        canvas.setFont(BODY_BOLD, 16); canvas.setFillColor(TEXT)
        canvas.drawString(68, H - 80, "RIOA")
        canvas.setFillColor(GOLDC)
        canvas.circle(68 + stringWidth("RIOA", BODY_BOLD, 16) + 5, H - 79, 1.9, fill=1, stroke=0)
        canvas.setFont(BODY_FONT, 8); canvas.setFillColor(MUTED)
        canvas.drawRightString(W - 68, H - 78, "rioaconsulting.com")
        ty = H * 0.62
        # title (wrap within the text column, shrink to fit 3 lines)
        main_title, _, subtitle = title.partition(" -- ")
        face, maxw = HEADING_DISPLAY, W - 136
        def wrap(text, size, maxlines=3):
            words, lines, cur = text.split(), [], ""
            for w in words:
                t = (cur + " " + w).strip()
                if stringWidth(t, face, size) <= maxw: cur = t
                else:
                    if cur: lines.append(cur)
                    cur = w
            if cur: lines.append(cur)
            return lines if len(lines) <= maxlines else None
        size, lines = 46.0, None
        while size >= 22 and not lines:
            lines = wrap(main_title, size); size -= 0 if lines else 2
        lines = lines or [main_title]
        # pill eyebrow
        eb = (eyebrow or "").strip()
        if eb:
            pw = stringWidth(eb, BODY_FONT, 8.5) + 26
            canvas.setStrokeColor(EDGE); canvas.setLineWidth(0.8)
            canvas.roundRect(68, ty + size * 0.92 + 16, pw, 21, 10.5, fill=0, stroke=1)
            canvas.setFont(BODY_FONT, 8.5); canvas.setFillColor(TEXT)
            canvas.drawString(81, ty + size * 0.92 + 23.2, eb)
        canvas.setFont(face, size); canvas.setFillColor(TEXT)
        for ln in lines:
            canvas.drawString(68, ty, ln); ty -= size * 1.06
        if subtitle:
            canvas.setFont(SITE_ITALIC, size * 0.78); canvas.setFillColor(TEXT)
            canvas.drawString(68, ty - 2, subtitle); ty -= size * 0.9
        canvas.setStrokeColor(GOLDC); canvas.setLineWidth(0.8)
        canvas.line(68, ty - 14, 128, ty - 14)
        # footer ledger
        canvas.setStrokeColor(EDGE); canvas.setLineWidth(0.5)
        canvas.line(68, 50, W - 68, 50)
        canvas.setFont(LEDGER_MONO, 7); canvas.setFillColor(MUTED)
        canvas.drawString(68, 37, classification)
        canvas.drawRightString(W - 68, 37, "RIOA  |  rioaconsulting.com")
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
        canvas.setFillColor(HexColor("#080807")); canvas.rect(0, 0, width, height, fill=1, stroke=0)

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
        canvas.setFont(LEDGER_MONO, 8)
        canvas.setFillColor(WARM_GRAY)
        canvas.drawString(2.4 * cm, 1.4 * cm, classification)
        canvas.drawRightString(width - 2.4 * cm, 1.4 * cm, f"Page {doc.page}")

        canvas.restoreState()

    return draw


_TOC_DIVIDER_RE = re.compile(r"(?i)^(part|appendix)\b")
_TOC_MODULE_RE = re.compile(r"(?i)^module\b")


class _TOCDoc(SimpleDocTemplate):
    """Same as SimpleDocTemplate, but records where PART/APPENDIX (H1) and
    Module (H2) headings land, so a table of contents can be built."""
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            sn = flowable.style.name
            txt = flowable.getPlainText().strip()
            if sn in ("H1", "H2") and _TOC_DIVIDER_RE.match(txt):
                self._toc_capture.append((0, txt, self.page))
            elif sn == "H2" and _TOC_MODULE_RE.match(txt):
                self._toc_capture.append((1, txt, self.page))


def _make_toc_flowables(entries, content_width):
    """Build the 'Contents' page from captured (level, text, page) tuples."""
    flows = [Paragraph("Contents", TOC_TITLE)]
    rows = []
    for level, text, page in entries:
        if level == 0:
            rows.append([Paragraph(escape_xml(text), TOC_PART),
                         Paragraph(str(page), TOC_PART_PAGE)])
        else:
            rows.append([Paragraph(escape_xml(text), TOC_MOD),
                         Paragraph(str(page), TOC_MOD_PAGE)])
    if rows:
        tbl = Table(rows, colWidths=[content_width - 36, 36])
        tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        flows.append(tbl)
    return flows


def _insert_toc(flows, toc_flows):
    """Insert the Contents page just before the first PART divider (on its
    own page), leaving the existing part page-break intact after it."""
    idx = None
    for j, fl in enumerate(flows):
        if isinstance(fl, Paragraph) and fl.style.name in ("H1", "H2") \
                and _TOC_DIVIDER_RE.match(fl.getPlainText().strip()):
            idx = j
            break
    if idx is None:
        return flows
    ins = idx - 1 if idx > 0 and isinstance(flows[idx - 1], PageBreak) else idx
    return flows[:ins] + [PageBreak()] + toc_flows + flows[ins:]


def convert(md_path: Path, pdf_path: Path, title: str,
            classification: str = "Client Confidential",
            eyebrow: str = "Websites for U.S. local businesses", chapter: str = "00"):
    text = md_path.read_text(encoding="utf-8")
    content_width = A4[0] - 2.4*cm - 2.4*cm
    cover = make_first_page_cover(title, classification, eyebrow, chapter)
    hf = make_header_footer(title, classification)

    def fresh_flows():
        # Fresh flowables each pass (reportlab consumes them on build). The
        # leading PageBreak pushes content past the cover banner.
        fl = md_to_flowables(text)
        fl.insert(0, PageBreak())
        return fl

    def build_once(flows):
        doc = _TOCDoc(
            str(pdf_path), pagesize=A4,
            title=title, author="RIOA Consulting",
            leftMargin=2.4*cm, rightMargin=2.4*cm,
            topMargin=2.5*cm, bottomMargin=2.5*cm,
        )
        doc._toc_capture = []
        doc.build(flows, onFirstPage=cover, onLaterPages=hf)
        return doc._toc_capture

    # 3-pass build so the TOC page numbers stay correct even though inserting
    # the Contents page shifts everything after it.
    entries = build_once(fresh_flows())                 # pass 1: pages w/o TOC
    if entries:
        toc = _make_toc_flowables(entries, content_width)
        entries2 = build_once(_insert_toc(fresh_flows(), toc))   # pass 2: pages w/ TOC
        toc = _make_toc_flowables(entries2, content_width)
        build_once(_insert_toc(fresh_flows(), toc))     # pass 3: final, correct numbers
    print(f"Wrote: {pdf_path}")


if __name__ == "__main__":
    # CLI usage:
    #   python _md_to_pdf_site.py <input.md> [output.pdf] ["Title"] ["Classification"]
    #
    # All args after the input path are optional. Defaults:
    #   output.pdf      -> input.md with .pdf extension
    #   Title           -> derived from filename
    #   Classification  -> "Client Confidential" (footer left)
    if len(sys.argv) < 2:
        print('Usage: python _md_to_pdf_site.py <input.md> [output.pdf] ["Title"] ["Classification"]')
        sys.exit(1)
    md_path = Path(sys.argv[1]).resolve()
    if not md_path.exists():
        print(f"Error: markdown file not found: {md_path}")
        sys.exit(1)
    pdf_path = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else md_path.with_suffix(".pdf")
    title = sys.argv[3] if len(sys.argv) >= 4 else md_path.stem.replace("_", " ").replace("-", " ")
    classification = sys.argv[4] if len(sys.argv) >= 5 else "Client Confidential"
    eyebrow = sys.argv[5] if len(sys.argv) >= 6 else "Websites for U.S. local businesses"
    chapter = sys.argv[6] if len(sys.argv) >= 7 else "00"
    convert(md_path, pdf_path, title, classification, eyebrow, chapter)
