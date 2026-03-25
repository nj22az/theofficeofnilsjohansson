#!/usr/bin/env python3
"""Convert JDS Markdown documents to PDF using WeasyPrint.

Usage: python3 md2pdf.py <input.md> [output.pdf]

If output.pdf is not specified, it will be created alongside the input file.
"""

import sys
import os
import markdown
from weasyprint import HTML

"""
JDS-PRO-007 Information Design Standard — CSS Implementation

Typography:     §4 — 4-level heading hierarchy, 10pt body, 1.5x line height
Fonts:          §4.3 — Source Sans Pro / Calibri / Inter (sans) + Consolas (mono)
Layout:         §5.1 — 25mm L/R margins, 20mm top, 25mm bottom (A4)
Alignment:      §5.2 — Left-align text, right-align numbers in tables
Colour:         §6.1 — Navy Blue (#1B3A5C), Steel Blue (#4A90A4), Warm Gray (#8C8C8C)
Uncontrolled:   PRO-005 §6 — Mark exported PDFs as UNCONTROLLED COPY
"""

CSS = """
/* ==========================================================================
   JDS-PRO-007 Compliant Stylesheet
   Colour palette: Navy Blue, Steel Blue, Warm Gray, White
   Fonts: Source Sans Pro (primary), Consolas (mono)
   ========================================================================== */

@page {
    size: A4;
    margin: 20mm 25mm 25mm 25mm;  /* §5.1: 25mm L/R, 20mm top, 25mm bottom */

    @top-left {
        content: string(doc-title);
        font-size: 7.5pt;
        color: #8C8C8C;  /* Warm Gray — §6.1 */
        font-family: 'Source Sans Pro', 'Calibri', 'Inter', sans-serif;
    }
    @top-right {
        content: "UNCONTROLLED COPY";  /* PRO-005 §6 */
        font-size: 7.5pt;
        color: #8C8C8C;
        font-family: 'Source Sans Pro', 'Calibri', 'Inter', sans-serif;
    }
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #8C8C8C;
        font-family: 'Source Sans Pro', 'Calibri', 'Inter', sans-serif;
    }
}

/* First page: no running header (title is already visible) */
@page :first {
    @top-left { content: none; }
}

body {
    font-family: 'Source Sans Pro', 'Calibri', 'Inter', sans-serif;  /* §4.3 */
    font-size: 10pt;       /* §4.2: 10–11pt */
    line-height: 1.5;      /* §4.2: 1.4–1.5x */
    color: #1a1a1a;
    max-width: 100%;
    text-align: left;      /* §5.2: Never justify */
}

/* --- Heading Hierarchy — §4.1 (4 levels max) --- */

h1 {
    font-size: 20pt;       /* §4.1: 18–22pt */
    font-weight: 700;
    color: #1B3A5C;        /* Navy Blue — §6.1 */
    border-bottom: 2pt solid #1B3A5C;
    padding-bottom: 6pt;
    margin-top: 0;
    margin-bottom: 12pt;
    string-set: doc-title content();  /* Feed into running header */
}

h2 {
    font-size: 14pt;       /* §4.1: 14–16pt */
    font-weight: 700;
    color: #1B3A5C;        /* Navy Blue */
    border-bottom: 0.75pt solid #4A90A4;  /* Steel Blue line below — §4.1 */
    padding-bottom: 4pt;
    margin-top: 18pt;
    margin-bottom: 8pt;
    page-break-after: avoid;
}

h3 {
    font-size: 12pt;       /* §4.1: 12–13pt */
    font-weight: 700;
    color: #4A90A4;        /* Steel Blue — §6.1 */
    margin-top: 14pt;
    margin-bottom: 6pt;
    page-break-after: avoid;
}

h4 {
    font-size: 11pt;       /* §4.1: 11–12pt */
    font-weight: 700;
    font-style: italic;    /* §4.1: Bold italic */
    color: #333;
    margin-top: 12pt;
    margin-bottom: 4pt;
}

/* --- Tables — §7.3 --- */

table {
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0;
    font-size: 9pt;        /* §4.2: never smaller than 9pt */
    page-break-inside: avoid;
}

th {
    background-color: #1B3A5C;  /* Navy Blue — §6.1 */
    color: white;
    font-weight: 600;
    text-align: left;      /* §5.2 */
    padding: 5pt 6pt;
    border: 1pt solid #1B3A5C;
}

td {
    padding: 5pt 6pt;      /* §7.3: generous cell padding */
    border: 1pt solid #ccc;
    vertical-align: top;
    text-align: left;      /* §5.2: left-align text */
}

/* §7.3: subtle alternating row shading */
tr:nth-child(even) {
    background-color: #f5f7fa;
}

/* Header metadata table (first table) — subdued styling for bento identity block */
table:first-of-type th,
table:first-of-type td {
    border: 1pt solid #999;
}
table:first-of-type th {
    background-color: #f0f0f0;
    color: #333;
}

/* --- Blockquotes (callouts) --- */

blockquote {
    border-left: 3pt solid #4A90A4;  /* Steel Blue */
    margin: 10pt 0;
    padding: 8pt 14pt;
    background-color: #f0f5f7;
    color: #333;
    font-style: italic;
}

/* --- Code — §4.3: monospace for codes and technical identifiers --- */

code {
    font-family: 'Consolas', 'Courier New', monospace;  /* §4.3 */
    background-color: #f5f5f5;
    padding: 1pt 3pt;
    font-size: 9pt;
    border-radius: 2pt;
}

pre {
    background-color: #f5f5f5;
    padding: 10pt;
    border: 1pt solid #ddd;
    border-radius: 3pt;
    font-size: 8.5pt;
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code {
    background: none;
    padding: 0;
}

/* --- Horizontal rules (section dividers — ma between sections) --- */

hr {
    border: none;
    border-top: 1pt solid #ccc;
    margin: 16pt 0;       /* §2 principle 1: Ma — meaningful white space */
}

strong {
    color: #1a1a1a;
}

/* --- Lists --- */

ul, ol {
    margin: 6pt 0;
    padding-left: 20pt;
}

li {
    margin-bottom: 3pt;
}

li input[type="checkbox"] {
    margin-right: 4pt;
}

/* --- Links — Steel Blue — §6.1 --- */

a {
    color: #4A90A4;
    text-decoration: none;
}

/* --- Paragraph spacing — §4.2: 6–8pt between paragraphs --- */

p {
    margin: 0 0 7pt 0;
}
"""


def md_to_pdf(input_path, output_path=None):
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
    )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><style>{CSS}</style></head>
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
