#!/usr/bin/env python3
"""JDS PDF Generator — JDS-PRO-007 Information Design Standard.

Converts JDS markdown documents to PDF with Japanese information design
principles: Ma (meaningful space), Bento (compartmented layout), Zukai
(visual clarity), and Monozukuri (visible craftsmanship).

Usage: python3 md2pdf.py <input.md> [output.pdf]
"""

import sys
import os
import re
import markdown
from weasyprint import HTML

# ---------------------------------------------------------------------------
# Extract document metadata from the markdown header table
# ---------------------------------------------------------------------------

def extract_metadata(md_text):
    """Pull Doc No, Rev, Status, Date, Author from the JDS header table."""
    meta = {}
    patterns = {
        'doc_no': r'\*\*Document No\.\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'revision': r'\*\*Revision\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'status': r'\*\*Status\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'date': r'\*\*Date\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'author': r'\*\*Author\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, md_text, re.MULTILINE)
        if match:
            meta[key] = match.group(1).strip()
    return meta


# ---------------------------------------------------------------------------
# JDS-PRO-007 Compliant Stylesheet — Japanese Information Design
#
# Design philosophy:
#   Ma (間)        — Space has meaning. No accidental emptiness.
#   Bento (弁当)   — Compact compartments. Each section self-contained.
#   Zukai (図解)   — Visual clarity through structure, not decoration.
#   Monozukuri     — Precision visible in every alignment and spacing choice.
#
# References: PRO-007 §3 (three-level reading), §4 (typography),
#             §5 (layout), §6 (colour), §7 (tables), §8 (Monozukuri)
# ---------------------------------------------------------------------------

CSS = """
/* === Page Setup — §5.1 ================================================= */

@page {{
    size: A4;
    margin: 22mm 22mm 20mm 22mm;

    @top-left {{
        content: "{doc_no}";
        font-size: 7.5pt;
        font-weight: 600;
        color: #1B3A5C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        letter-spacing: 0.5pt;
    }}
    @top-center {{
        content: string(doc-title);
        font-size: 7pt;
        color: #8C8C8C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
    }}
    @top-right {{
        content: "UNCONTROLLED COPY";
        font-size: 6.5pt;
        color: #aaa;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        letter-spacing: 0.3pt;
        text-transform: uppercase;
    }}
    @bottom-left {{
        content: "Rev {revision}";
        font-size: 7pt;
        color: #8C8C8C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
    }}
    @bottom-center {{
        content: "Page " counter(page) " of " counter(pages);
        font-size: 7.5pt;
        color: #8C8C8C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
    }}
    @bottom-right {{
        content: "{date}";
        font-size: 7pt;
        color: #8C8C8C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
    }}
}}

/* First page: doc number but no title in header (visible in body) */
@page :first {{
    @top-center {{ content: none; }}
}}

/* === Body — §4.2 ======================================================= */

body {{
    font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #222;
    text-align: left;
    orphans: 3;
    widows: 3;
}}

/* === Heading Hierarchy — §4.1 (4 levels) =============================== */

h1 {{
    font-size: 18pt;
    font-weight: 700;
    color: #1B3A5C;
    border-bottom: 1.5pt solid #1B3A5C;
    padding-bottom: 5pt;
    margin: 0 0 4pt 0;
    string-set: doc-title content();
    letter-spacing: -0.3pt;
}}

h2 {{
    font-size: 14pt;
    font-weight: 700;
    color: #1B3A5C;
    border-bottom: 0.5pt solid #ccc;
    padding-bottom: 3pt;
    margin: 20pt 0 7pt 0;
    page-break-after: avoid;
}}

h3 {{
    font-size: 11.5pt;
    font-weight: 600;
    color: #4A90A4;
    margin: 14pt 0 5pt 0;
    page-break-after: avoid;
}}

h4 {{
    font-size: 10.5pt;
    font-weight: 600;
    font-style: italic;
    color: #444;
    margin: 10pt 0 4pt 0;
}}

/* === Metadata Table (first table) — Bento Identity Block =============== */
/* Compact, refined. Not a data table — an identity strip. */

table:first-of-type {{
    width: auto;
    min-width: 55%;
    max-width: 75%;
    margin: 6pt 0 14pt 0;
    font-size: 8.5pt;
    border: none;
    border-top: 2pt solid #1B3A5C;
    border-bottom: 1pt solid #ccc;
}}

table:first-of-type th,
table:first-of-type td {{
    border: none;
    border-bottom: 0.5pt solid #e0e0e0;
    padding: 3pt 8pt;
    background: none;
}}

table:first-of-type th {{
    background: none;
    color: #8C8C8C;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 7pt;
    letter-spacing: 0.5pt;
    width: 30%;
    vertical-align: top;
}}

table:first-of-type td {{
    color: #222;
    font-weight: 500;
}}

table:first-of-type tr:nth-child(even) {{
    background: none;
}}

table:first-of-type tr:last-child th,
table:first-of-type tr:last-child td {{
    border-bottom: none;
}}

/* === Data Tables — §7.3 ================================================ */
/* Light header, clean lines. Not heavy navy blocks — refined precision. */

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 6pt 0 10pt 0;
    font-size: 9pt;
    page-break-inside: avoid;
    border-top: 1.5pt solid #1B3A5C;
    border-bottom: 1pt solid #1B3A5C;
}}

th {{
    background-color: #f0f3f6;
    color: #1B3A5C;
    font-weight: 600;
    font-size: 8.5pt;
    text-align: left;
    text-transform: uppercase;
    letter-spacing: 0.3pt;
    padding: 5pt 6pt;
    border-bottom: 1pt solid #1B3A5C;
    border-left: none;
    border-right: none;
}}

td {{
    padding: 4pt 6pt;
    border-bottom: 0.5pt solid #e0e0e0;
    border-left: none;
    border-right: none;
    vertical-align: top;
    text-align: left;
}}

tr:nth-child(even) {{
    background-color: #fafbfc;
}}

tr:last-child td {{
    border-bottom: none;
}}

/* === Horizontal Rules — Ma Dividers ==================================== */

hr {{
    border: none;
    border-top: 0.5pt solid #ddd;
    margin: 14pt 0;
}}

/* === Blockquotes — Callout Strips ====================================== */

blockquote {{
    border-left: 2pt solid #4A90A4;
    margin: 8pt 0;
    padding: 6pt 12pt;
    background-color: #f7f9fb;
    color: #333;
    font-size: 9.5pt;
    font-style: italic;
}}

blockquote p {{
    margin: 0 0 4pt 0;
}}

/* === Code — §4.3 ======================================================= */

code {{
    font-family: 'DejaVu Sans Mono', 'Consolas', monospace;
    background-color: #f5f5f5;
    padding: 0.5pt 2.5pt;
    font-size: 8.5pt;
    border-radius: 1.5pt;
    color: #1B3A5C;
}}

pre {{
    background-color: #f8f8f8;
    padding: 8pt 10pt;
    border-left: 2pt solid #ccc;
    border-radius: 0;
    font-size: 8pt;
    line-height: 1.4;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 6pt 0 10pt 0;
}}

pre code {{
    background: none;
    padding: 0;
    color: #333;
}}

/* === Lists ============================================================= */

ul, ol {{
    margin: 4pt 0 6pt 0;
    padding-left: 18pt;
}}

li {{
    margin-bottom: 2pt;
    line-height: 1.45;
}}

li input[type="checkbox"] {{
    margin-right: 3pt;
}}

/* === Links — Steel Blue ================================================ */

a {{
    color: #4A90A4;
    text-decoration: none;
}}

/* === Paragraphs — §4.2 ================================================= */

p {{
    margin: 0 0 6pt 0;
}}

strong {{
    color: #111;
    font-weight: 600;
}}

/* === Print helpers ====================================================== */

h2, h3 {{
    page-break-after: avoid;
}}

table, pre, blockquote {{
    page-break-inside: avoid;
}}
"""


def md_to_pdf(input_path, output_path=None):
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Extract metadata for page headers/footers
    meta = extract_metadata(md_content)
    doc_no = meta.get('doc_no', '')
    revision = meta.get('revision', '')
    date = meta.get('date', '')

    # Format CSS with metadata
    formatted_css = CSS.format(
        doc_no=doc_no,
        revision=revision,
        date=date,
    )

    html_content = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
    )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><style>{formatted_css}</style></head>
<body>{html_content}</body>
</html>"""

    HTML(string=full_html).write_pdf(output_path)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 md2pdf.py <input.md> [output.pdf]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    result = md_to_pdf(input_file, output_file)
    print(f"PDF created: {result}")
