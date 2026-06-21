"""Converter test suite: runs every registered converter against a sample fixture
and checks options validation and edge cases.

Usage: .venv\\Scripts\\python tests/test_converters.py
"""
import sys
import unittest
import shutil
import json
from pathlib import Path
import pandas as pd
from docx import Document
from reportlab.pdfgen import canvas

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.converters import _REGISTRY, get_converter
from app.converters.text_converters.options import PdfOptions
from app.converters.image_converters.shared import JpgOptions, PngOptions
from app.converters.data_converters.csv_to_json import CsvToJsonOptions

FIXTURES_DIR = project_root / "tests" / "fixtures"
OUTPUT_DIR = project_root / "tests" / "output"

SAMPLE_MD = """# Test Document

This is a test of **Adla-Badli** conversion.

## Features

- Bullet point 1
- Bullet point 2
"""

SAMPLE_TXT = """Adla-Badli Plain Text Sample

This is the first paragraph.
"""

SAMPLE_HTML = """<!DOCTYPE html>
<html><head><title>Sample</title></head>
<body>
<h1>HTML Sample Document</h1>
<p>A paragraph with <strong>bold</strong> text.</p>
</body></html>
"""

SAMPLE_CSV = """name,department,salary,start_date
Aarav Sharma,Engineering,95000.1234,2021-03-15
Diya Patel,Design,78000.5678,2022-07-01
"""

SAMPLE_JSON = """[
  {"id": 1, "name": "Aarav", "salary": 95000.1234},
  {"id": 2, "name": "Diya", "salary": 78000.5678}
]
"""

SAMPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" width="200" height="100">
  <rect width="100%" height="100%" fill="#FAF7F2" />
  <circle cx="60" cy="50" r="35" fill="#C4714A" />
</svg>"""


class TestConverters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Write text-based fixtures
        cls.fixture_paths = {
            "md": FIXTURES_DIR / "sample.md",
            "txt": FIXTURES_DIR / "sample.txt",
            "html": FIXTURES_DIR / "sample.html",
            "csv": FIXTURES_DIR / "sample.csv",
            "json": FIXTURES_DIR / "sample.json",
            "svg": FIXTURES_DIR / "sample.svg",
        }
        cls.fixture_paths["md"].write_text(SAMPLE_MD, encoding="utf-8")
        cls.fixture_paths["txt"].write_text(SAMPLE_TXT, encoding="utf-8")
        cls.fixture_paths["html"].write_text(SAMPLE_HTML, encoding="utf-8")
        cls.fixture_paths["csv"].write_text(SAMPLE_CSV, encoding="utf-8")
        cls.fixture_paths["json"].write_text(SAMPLE_JSON, encoding="utf-8")
        cls.fixture_paths["svg"].write_text(SAMPLE_SVG, encoding="utf-8")

        # Generate binary fixtures programmatically
        cls.fixture_paths["docx"] = FIXTURES_DIR / "sample.docx"
        doc = Document()
        doc.add_paragraph("This is a dummy docx paragraph.")
        doc.save(str(cls.fixture_paths["docx"]))

        cls.fixture_paths["xlsx"] = FIXTURES_DIR / "sample.xlsx"
        df = pd.DataFrame([{"col1": "val1", "col2": "val2"}])
        df.to_excel(cls.fixture_paths["xlsx"], index=False, engine="openpyxl")

        cls.fixture_paths["pdf"] = FIXTURES_DIR / "sample.pdf"
        c = canvas.Canvas(str(cls.fixture_paths["pdf"]))
        c.drawString(100, 750, "This is a dummy PDF line.")
        c.save()

    @classmethod
    def tearDownClass(cls):
        # Leave fixtures intact (as requested to keep fixtures committed),
        # but purge outputs
        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)

    def test_all_registered_converters(self):
        """Test all registered registry paths produce non-empty files."""
        for (source_ext, target_ext) in _REGISTRY:
            label = f"{source_ext} -> {target_ext}"
            input_path = self.fixture_paths.get(source_ext)
            self.assertIsNotNone(input_path, f"No fixture for source extension: {source_ext}")

            output_path = OUTPUT_DIR / f"test_{source_ext}.{target_ext}"
            if output_path.exists():
                output_path.unlink()

            converter = get_converter(source_ext, target_ext)
            converter.convert(input_path, output_path)

            self.assertTrue(output_path.exists(), f"Output file not created for {label}")
            self.assertGreater(output_path.stat().st_size, 0, f"Output file is empty for {label}")

    def test_converter_options(self):
        """Verify custom options parameter validation and logic mapping."""
        # 1. Text PDF options
        opts_pdf = PdfOptions(page_size="letter", font_size=14, margin=3.0)
        md_pdf_conv = get_converter("md", "pdf")
        out_pdf = OUTPUT_DIR / "options_test.pdf"
        md_pdf_conv.convert(self.fixture_paths["md"], out_pdf, options=opts_pdf)
        self.assertTrue(out_pdf.exists())

        # 2. Image JPEG options
        opts_jpg = JpgOptions(bg_color="dark", dpi=300, quality=80)
        svg_jpg_conv = get_converter("svg", "jpg")
        out_jpg = OUTPUT_DIR / "options_test.jpg"
        svg_jpg_conv.convert(self.fixture_paths["svg"], out_jpg, options=opts_jpg)
        self.assertTrue(out_jpg.exists())

        # 3. Image PNG options
        opts_png = PngOptions(bg_color="black", dpi=100, compression=8)
        svg_png_conv = get_converter("svg", "png")
        out_png = OUTPUT_DIR / "options_test.png"
        svg_png_conv.convert(self.fixture_paths["svg"], out_png, options=opts_png)
        self.assertTrue(out_png.exists())

    def test_edge_case_empty_input(self):
        """Gracefully handle empty (0-byte) source files without raising internal crashes."""
        empty_path = FIXTURES_DIR / "empty.csv"
        empty_path.write_bytes(b"")

        csv_xlsx_conv = get_converter("csv", "xlsx")
        out_xlsx = OUTPUT_DIR / "empty_out.xlsx"
        
        # Should raise ValueError rather than general crash
        with self.assertRaises(ValueError):
            csv_xlsx_conv.convert(empty_path, out_xlsx)

    def test_edge_case_malformed_csv(self):
        """Malformed CSV (unclosed quote) raises ValueError or parsing exception."""
        malformed_csv = FIXTURES_DIR / "malformed.csv"
        malformed_csv.write_text('name,age\n"Aarav,20\n', encoding="utf-8") # Unclosed quote
        
        csv_json_conv = get_converter("csv", "json")
        out_json = OUTPUT_DIR / "malformed_out.json"
        
        with self.assertRaises(Exception):
            csv_json_conv.convert(malformed_csv, out_json)

    def test_edge_case_invalid_json(self):
        """Invalid JSON syntax returns a clean validation error."""
        invalid_json = FIXTURES_DIR / "invalid.json"
        invalid_json.write_text('{"name": "Aarav",}', encoding="utf-8") # Trailing comma syntax error
        
        json_csv_conv = get_converter("json", "csv")
        out_csv = OUTPUT_DIR / "invalid_out.csv"
        
        with self.assertRaises(Exception):
            json_csv_conv.convert(invalid_json, out_csv)

    def test_edge_case_svg_no_viewbox(self):
        """SVG lacking viewBox handles conversion gracefully."""
        no_viewbox_svg = FIXTURES_DIR / "no_viewbox.svg"
        no_viewbox_svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'
            '<circle cx="50" cy="50" r="40" fill="blue"/>'
            '</svg>', 
            encoding="utf-8"
        )
        
        svg_png_conv = get_converter("svg", "png")
        out_png = OUTPUT_DIR / "no_viewbox.png"
        svg_png_conv.convert(no_viewbox_svg, out_png)
        self.assertTrue(out_png.exists())

    def test_edge_case_long_filename(self):
        """Handles extremely long filenames (255 characters) gracefully."""
        long_stem = "a" * 240
        long_filename = f"{long_stem}.md"
        long_path = FIXTURES_DIR / long_filename
        long_path.write_text("# Hello", encoding="utf-8")

        md_html_conv = get_converter("md", "html")
        out_html = OUTPUT_DIR / f"{long_stem}.html"
        
        try:
            md_html_conv.convert(long_path, out_html)
            self.assertTrue(out_html.exists())
        finally:
            if long_path.exists():
                long_path.unlink()
            if out_html.exists():
                out_html.unlink()


if __name__ == "__main__":
    unittest.main()

