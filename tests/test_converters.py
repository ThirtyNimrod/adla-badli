"""Converter test suite: runs every registered converter against a sample fixture.

Usage: .venv\\Scripts\\python tests/test_converters.py
Exits non-zero if any conversion fails or produces an empty file.
"""
import sys
import traceback
from pathlib import Path

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.converters import _REGISTRY, get_converter

FIXTURES_DIR = project_root / "tests" / "fixtures"
OUTPUT_DIR = project_root / "tests" / "output"

SAMPLE_MD = """# Test Document

This is a test of **Adla-Badli** conversion.

## Features

- Bullet point 1
- Bullet point 2

> A blockquote with a [link](https://example.com).

| Name | Value |
|------|-------|
| Alpha | 1 |
| Beta | 2 |
"""

SAMPLE_TXT = """Adla-Badli Plain Text Sample

This is the first paragraph of a plain text document. It has enough
content to span multiple lines and verify paragraph handling.

This is the second paragraph, separated by a blank line.
"""

SAMPLE_HTML = """<!DOCTYPE html>
<html><head><title>Sample</title></head>
<body>
<h1>HTML Sample Document</h1>
<p>A paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
<ul><li>Item one</li><li>Item two</li></ul>
<table><tr><th>Key</th><th>Value</th></tr><tr><td>x</td><td>1</td></tr></table>
</body></html>
"""

SAMPLE_CSV = """name,department,salary,start_date
Aarav Sharma,Engineering,95000,2021-03-15
Diya Patel,Design,78000,2022-07-01
Rohan Gupta,Marketing,68000,2020-11-20
Priya Singh,Engineering,102000,2019-05-09
"""

SAMPLE_JSON = """[
  {"id": 1, "name": "Aarav", "contact": {"email": "aarav@example.com", "city": "Mumbai"}, "tags": ["lead", "eng"]},
  {"id": 2, "name": "Diya", "contact": {"email": "diya@example.com", "city": "Pune"}, "tags": ["design"]},
  {"id": 3, "name": "Rohan", "contact": {"email": "rohan@example.com", "city": "Delhi"}, "tags": []}
]
"""

SAMPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" width="200" height="100">
  <rect width="100%" height="100%" fill="#FAF7F2" />
  <circle cx="60" cy="50" r="35" fill="#C4714A" />
  <rect x="110" y="20" width="60" height="60" fill="#2E2018" rx="4" />
</svg>"""

FIXTURES = {
    "md": ("sample.md", SAMPLE_MD),
    "txt": ("sample.txt", SAMPLE_TXT),
    "html": ("sample.html", SAMPLE_HTML),
    "csv": ("sample.csv", SAMPLE_CSV),
    "json": ("sample.json", SAMPLE_JSON),
    "svg": ("sample.svg", SAMPLE_SVG),
}


def write_fixtures() -> dict:
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    paths = {}
    for ext, (filename, content) in FIXTURES.items():
        path = FIXTURES_DIR / filename
        path.write_text(content, encoding="utf-8")
        paths[ext] = path
    return paths


def run_all() -> int:
    fixture_paths = write_fixtures()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    passed, failed = [], []

    for (source_ext, target_ext) in sorted(_REGISTRY):
        label = f"{source_ext} -> {target_ext}"
        input_path = fixture_paths.get(source_ext)
        if input_path is None:
            failed.append((label, f"No fixture defined for source .{source_ext}"))
            continue

        output_path = OUTPUT_DIR / f"sample_{source_ext}.{target_ext}"
        if output_path.exists():
            output_path.unlink()

        try:
            converter = get_converter(source_ext, target_ext)
            converter.convert(input_path, output_path)
            if not output_path.exists():
                failed.append((label, "Output file was not created"))
            elif output_path.stat().st_size == 0:
                failed.append((label, "Output file is empty"))
            else:
                passed.append((label, output_path.stat().st_size))
        except Exception as exc:
            failed.append((label, f"{type(exc).__name__}: {exc}"))
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"CONVERTER TEST RESULTS  ({len(passed)} passed, {len(failed)} failed)")
    print("=" * 60)
    for label, size in passed:
        print(f"  PASS  {label:<16} ({size:,} bytes)")
    for label, reason in failed:
        print(f"  FAIL  {label:<16} {reason}")
    print("=" * 60)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run_all())
