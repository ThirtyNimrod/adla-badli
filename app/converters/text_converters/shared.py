"""Shared helpers for the text converter group (md, txt, html sources).

All text conversions flow through Pandoc (via pypandoc). PDF output is
rendered with xhtml2pdf (pure Python, no GTK system dependencies), using
Pandoc's HTML output as the intermediate representation.
"""
from pathlib import Path
from typing import Literal

import pypandoc
from xhtml2pdf import pisa

PageSize = Literal["a4", "letter"]

# Base stylesheet applied to standalone HTML output and the PDF pipeline.
# Kept deliberately print-like: serif body, comfortable measure, restrained color.
_DOCUMENT_CSS = """
body {
    font-family: Georgia, 'Times New Roman', serif;
    color: #2E2018;
    line-height: 1.6;
    font-size: 11pt;
}
h1, h2, h3, h4 { color: #2E2018; line-height: 1.25; }
h1 { font-size: 22pt; }
h2 { font-size: 16pt; }
h3 { font-size: 13pt; }
code, pre {
    font-family: 'Courier New', monospace;
    font-size: 9.5pt;
    background-color: #F5F1EA;
}
pre { padding: 8px; }
blockquote {
    border-left: 3px solid #C4714A;
    margin-left: 0;
    padding-left: 14px;
    color: #6B5A50;
}
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #D8CFC4; padding: 6px 8px; text-align: left; }
th { background-color: #F5F1EA; }
a { color: #C4714A; }
hr { border: none; border-top: 1px solid #D8CFC4; }
"""


def _pdf_page_css(page_size: PageSize) -> str:
    size = "A4" if page_size == "a4" else "letter"
    return f"@page {{ size: {size}; margin: 2cm; }}\n" + _DOCUMENT_CSS


def read_source_as_html(input_path: Path, source_format: str) -> str:
    """Converts a source file to an HTML body string via Pandoc.

    source_format is a pandoc reader name (e.g. 'markdown', 'html').
    Plain .txt files should be read with the 'markdown' reader: plain
    text is valid markdown, and this preserves paragraph structure.
    """
    return pypandoc.convert_file(str(input_path), to="html", format=source_format)


def html_to_pdf_file(html_body: str, output_path: Path, page_size: PageSize = "a4", title: str = "Document") -> None:
    """Renders an HTML body string to a PDF file using xhtml2pdf."""
    document = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title><style>{_pdf_page_css(page_size)}</style></head>"
        f"<body>{html_body}</body></html>"
    )
    with output_path.open("wb") as fh:
        result = pisa.CreatePDF(src=document, dest=fh, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"PDF rendering failed with {result.err} error(s).")


def wrap_html_document(html_body: str, title: str = "Document") -> str:
    """Wraps an HTML body in a complete standalone document with base styling."""
    return (
        "<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='utf-8'>\n"
        f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
        f"<title>{title}</title>\n<style>{_DOCUMENT_CSS}</style>\n</head>\n"
        f"<body>\n{html_body}\n</body>\n</html>\n"
    )


def convert_via_pandoc(input_path: Path, output_path: Path, source_format: str, target_format: str) -> None:
    """Direct file-to-file Pandoc conversion for formats pandoc writes natively."""
    pypandoc.convert_file(
        source_file=str(input_path),
        to=target_format,
        format=source_format,
        outputfile=str(output_path),
    )


def convert_to_plain_text(input_path: Path, output_path: Path, source_format: str) -> None:
    """Extracts readable plain text from a source document via Pandoc's plain writer."""
    text = pypandoc.convert_file(str(input_path), to="plain", format=source_format)
    output_path.write_text(text, encoding="utf-8")
