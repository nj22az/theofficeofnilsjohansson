#!/usr/bin/env python3
"""Convert JDS Markdown documents to PDF using WeasyPrint.

Usage: python3 md2pdf.py <input.md> [output.pdf]

If output.pdf is not specified, it will be created alongside the input file.
"""

import sys
import os
import markdown
from weasyprint import HTML

CSS = """
@page {
    size: A4;
    margin: 20mm 18mm 25mm 18mm;
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #666;
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    }
    @top-right {
        content: "UNCONTROLLED COPY — FOR REFERENCE ONLY";
        font-size: 7pt;
        color: #999;
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    }
}

body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.4;
    color: #1a1a1a;
    max-width: 100%;
}

h1 {
    font-size: 16pt;
    color: #1B3A5C;
    border-bottom: 2px solid #1B3A5C;
    padding-bottom: 4pt;
    margin-top: 0;
}

h2 {
    font-size: 13pt;
    color: #1B3A5C;
    border-bottom: 1px solid #4A90A4;
    padding-bottom: 3pt;
    margin-top: 16pt;
    page-break-after: avoid;
}

h3 {
    font-size: 11pt;
    color: #4A90A4;
    margin-top: 12pt;
    page-break-after: avoid;
}

h4 {
    font-size: 10pt;
    color: #333;
    margin-top: 10pt;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 8pt 0;
    font-size: 9pt;
    page-break-inside: avoid;
}

th {
    background-color: #1B3A5C;
    color: white;
    font-weight: 600;
    text-align: left;
    padding: 5pt 6pt;
    border: 1px solid #1B3A5C;
}

td {
    padding: 4pt 6pt;
    border: 1px solid #ccc;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #f5f7fa;
}

/* Header metadata table — no colored header */
table:first-of-type th,
table:first-of-type td {
    border: 1px solid #999;
}
table:first-of-type th {
    background-color: #f0f0f0;
    color: #333;
}

blockquote {
    border-left: 3px solid #4A90A4;
    margin: 10pt 0;
    padding: 6pt 12pt;
    background-color: #f0f5f7;
    color: #333;
    font-style: italic;
}

code {
    font-family: 'Consolas', 'Courier New', monospace;
    background-color: #f5f5f5;
    padding: 1pt 3pt;
    font-size: 9pt;
    border-radius: 2pt;
}

pre {
    background-color: #f5f5f5;
    padding: 8pt;
    border: 1px solid #ddd;
    border-radius: 3pt;
    font-size: 8.5pt;
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code {
    background: none;
    padding: 0;
}

hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 14pt 0;
}

strong {
    color: #1a1a1a;
}

ul, ol {
    margin: 4pt 0;
    padding-left: 20pt;
}

li {
    margin-bottom: 2pt;
}

/* Checkbox styling */
li input[type="checkbox"] {
    margin-right: 4pt;
}

a {
    color: #4A90A4;
    text-decoration: none;
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
