# Adla-Badli File Converter Suite

FastAPI-powered universal file converter: bridges AI-friendly formats (md, txt, html, csv, json, svg) with human-friendly ones (docx, pdf, xlsx, html, jpg, png).

## Conversion Matrix (21 paths)

| From \ To | DOCX | PDF | XLSX | CSV | JSON | HTML | TXT | JPG | PNG |
|-----------|:----:|:---:|:----:|:---:|:----:|:----:|:---:|:---:|:---:|
| **md**    | ✅ | ✅ | — | — | — | ✅ | ✅ | — | — |
| **txt**   | ✅ | ✅ | — | — | — | ✅ | — | — | — |
| **html**  | ✅ | ✅ | — | — | — | — | ✅ | — | — |
| **csv**   | ✅ | ✅ | ✅ | — | ✅ | — | — | — | — |
| **json**  | ✅ | ✅ | ✅ | ✅ | — | — | — | — | — |
| **svg**   | — | ✅ | — | — | — | — | — | ✅ | ✅ |

Converters are organized into three groups under `app/converters/`:

- `text_converters/` — Pandoc-driven document conversion; PDFs rendered with xhtml2pdf
- `data_converters/` — pandas normalization rendered via openpyxl, python-docx, and ReportLab
- `image_converters/` — svglib rasterization (Pillow finishing) and vector-preserving PDF export

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