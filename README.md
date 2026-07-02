# Adla-Badli File Converter Suite

FastAPI-powered universal file converter: bridges AI-friendly formats (md, txt, html, csv, json, svg, webp) with human-friendly ones (docx, pdf, xlsx, html, jpg, png).

## Conversion Matrix (23 paths)

| From \ To | DOCX | PDF | XLSX | CSV | JSON | HTML | TXT | JPG | PNG |
|-----------|:----:|:---:|:----:|:---:|:----:|:----:|:---:|:---:|:---:|
| **md**    | ✅ | ✅ | — | — | — | ✅ | ✅ | — | — |
| **txt**   | ✅ | ✅ | — | — | — | ✅ | — | — | — |
| **html**  | ✅ | ✅ | — | — | — | — | ✅ | — | — |
| **csv**   | ✅ | ✅ | ✅ | — | ✅ | — | — | — | — |
| **json**  | ✅ | ✅ | ✅ | ✅ | — | — | — | — | — |
| **svg**   | — | ✅ | — | — | — | — | — | ✅ | ✅ |
| **webp**  | — | — | — | — | — | — | — | ✅ | ✅ |

Converters are organized into three groups under `app/converters/`:

- `text_converters/` — Pandoc-driven document conversion; PDFs rendered with xhtml2pdf
- `data_converters/` — pandas normalization rendered via openpyxl, python-docx, and ReportLab
- `image_converters/` — SVG and WebP processing (Pillow rasterization, svglib vector-preserving PDF export)

## Key Features

- **23 Conversion Paths**: Supports bridging Markdown, plain text, HTML, CSV, JSON, SVG, and WebP files to DOCX, PDF, XLSX, CSV, JSON, HTML, TXT, JPG, and PNG.
- **100% Private & Local**: Zero cloud dependencies or telemetry; runs entirely on localhost.
- **Self-Documenting Pydantic Schema**: Dynamic option fields (e.g. PDF page size, JSON structure, image background color) are auto-generated from Pydantic schemas.
- **Interactive File Previewer**: Instant inline previewing of converted results directly in the browser:
  - **Images (PNG, JPG, SVG)**: Displayed within a styled viewer.
  - **PDF & HTML**: Structured layout rendering in a sandboxed iframe.
  - **CSV**: Renders a dynamic, paginated preview table (first 10 rows).
  - **JSON & TXT**: Formatted plain text codeblocks (JSON is pretty-printed).
  - **DOCX & XLSX**: Styled placeholder fallback reminding the user to download.
- **Workspace Lifecycle Management**: Clean, UUID-isolated conversion workspaces with deferred background cleanup tasks to prevent file accumulation.

## Documentation

See the [Documentation Index](docs/README.md) for details.

- [Quick Start Guide](docs/core/quick_start.md)
- [Architecture Documentation](docs/core/architecture.md)
- [Troubleshooting Guide](docs/core/troubleshooting.md)

## Installation Quick Summary

Ensure you have Python 3.10+ installed.

```bash
# Setup virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/macOS

# Install uv & dependencies
pip install uv
uv pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```bash
# Runs every registered converter against generated fixtures
.venv\Scripts\python tests/test_converters.py
.venv\Scripts\python tests/test_workspace.py
```

## Contributors & AI Collaborators

Special thanks to my AI pair programming partners who helped design, build, and troubleshoot this suite:

- **Claude Code** (Anthropic) — Assisted with architecture refactoring, E2E test environments, and frontend polish.
- **Gemini CLI / Antigravity** (Google DeepMind) — Assisted with file preview features, troubleshooting system dependencies, and guide index setups.