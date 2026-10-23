#!/usr/bin/env python3
"""
RIOA Brand PDF builder.
Usage:  python3 build_pdf.py input.html "/Users/vik/RIOA/Output_Name.pdf"
Renders an HTML file to PDF and runs a voice/quality guard (no em/en dashes).
Requires: pip install weasyprint --break-system-packages
"""
import sys, re

def main():
    if len(sys.argv) < 3:
        print("usage: python3 build_pdf.py input.html output.pdf"); sys.exit(1)
    src, out = sys.argv[1], sys.argv[2]

    html = open(src, encoding="utf-8").read()

    # HARD BAN guard: em-dash (U+2014) and en-dash (U+2013) must not appear
    bad = html.count("—") + html.count("–")
    if bad:
        print(f"WARNING: {bad} em/en dash(es) found. Vik's voice profile bans these. "
              f"Replace with ellipses, commas, periods, parentheses, or '/' before shipping.")

    from weasyprint import HTML
    HTML(string=html, base_url=".").write_pdf(out)

    try:
        from pypdf import PdfReader
        print(f"OK -> {out}  ({len(PdfReader(out).pages)} pages)")
    except Exception:
        print(f"OK -> {out}")

if __name__ == "__main__":
    main()
