# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Adla-Badli** is a FastAPI-powered file converter suite providing a localhost web UI for 21 conversion paths between AI-friendly (md, txt, html, csv, json, svg) and human-friendly (docx, pdf, xlsx, html, jpg, png) formats. All conversions run locally with no external cloud dependencies.

## Commands

### Setup
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Unix/macOS
pip install uv
uv pip install -r requirements.txt
```

### Run
```bash
uvicorn app.main:app --reload
# http://127.0.0.1:8000
```

### Tests
```bash
# Python unit tests (converters + workspace lifecycle)
.venv\Scripts\python tests/test_converters.py
.venv\Scripts\python tests/test_workspace.py

# Playwright E2E (auto-starts Uvicorn)
npm run test:e2e          # headless
npm run test:e2e:ui       # interactive
npm run test:e2e:debug    # step-through
```

## Architecture

### Request Lifecycle
1. Client POSTs file + target extension to `/api/convert`
2. `main.py` extracts source extension, calls `get_converter(source_ext, target_ext)` from the registry
3. `ConversionWorkspace` creates a UUID-named temp directory
4. Converter runs synchronously: `converter.convert(input_path, output_path, **options)`
5. `FileResponse` streams the result; `workspace.release()` defers cleanup to `BackgroundTasks`

### Converter Registry (`app/converters/__init__.py`)
Converters self-register at import time via `(source_ext, target_ext)` tuples. Three groups:
- **`text_converters/`** — Pandoc drives md/txt/html → docx/html/txt; xhtml2pdf handles PDF output
- **`data_converters/`** — pandas normalizes csv/json; openpyxl (xlsx), python-docx (docx), ReportLab (pdf) render output
- **`image_converters/`** — svglib + Pillow rasterize svg → jpg/png; svglib + ReportLab preserve vectors for svg → pdf

### Frontend (`app/static/js/main.js`)
On load, fetches `/api/converters` once and caches results. When a file is dropped, JS filters cached converters by source extension and populates the target dropdown. `options_schema` from each converter (a JSON Schema object) is used to dynamically render form controls — no hardcoded form definitions exist.

### Workspace (`app/workspace.py`)
`ConversionWorkspace` is a context manager. Call `workspace.release()` before returning the `FileResponse` to hand off cleanup to FastAPI `BackgroundTasks`, which deletes the temp directory after the response finishes streaming.

## Adding a New Converter

1. Create `app/converters/<group>_converters/source_to_target.py` inheriting `BaseConverter` (`app/converters/base.py`):
   ```python
   from app.converters.base import BaseConverter

   class SourceToTargetConverter(BaseConverter):
       @property
       def source_extension(self) -> str: return "source"
       @property
       def target_extension(self) -> str: return "target"
       def convert(self, input_path, output_path, **kwargs) -> None: ...
   ```
2. Import and append to the converter list in the group's `__init__.py`.
3. The frontend updates automatically — `/api/converters` reflects the new path immediately.
4. Add a fixture and test case to `tests/test_converters.py`.

## Key Files

| File | Role |
|------|------|
| `app/main.py` | All HTTP routes and request/response handling |
| `app/converters/__init__.py` | Registry: `get_converter()`, `list_converters()` |
| `app/converters/base.py` | `BaseConverter` abstract class |
| `app/workspace.py` | Temp file lifecycle and deferred cleanup |
| `app/static/js/main.js` | All client-side logic including dynamic form rendering |
| `app/templates/index.html` | Single-page app markup |
| `docs/core/architecture.md` | Extended architecture diagrams |
| `docs/core/troubleshooting.md` | Port conflicts, Pandoc, Playwright, Windows policy issues |
