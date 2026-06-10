# Quick Start Guide

This guide helps you set up and run the Adla-Badli File Converter Suite.

## Prerequisites

- Python 3.10 or higher
- **Pandoc** — required for all text format conversions (md, txt, html → docx/pdf/html/txt).
  - Fastest: `python -c "import pypandoc; pypandoc.download_pandoc()"` (downloads the binary automatically via pypandoc-binary)
  - Or install system-wide: `winget install JohnMacFarlane.Pandoc` (Windows) · `brew install pandoc` (macOS) · `sudo apt install pandoc` (Ubuntu)

## Installation

1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   > `uv` is optional but faster: `pip install uv && uv pip install -r requirements.txt`

## Running the Application

```bash
uvicorn app.main:app --reload
```

Open your browser at `http://127.0.0.1:8000`.

## Supported Conversions (21 paths)

| From \ To | DOCX | PDF | XLSX | CSV | JSON | HTML | TXT | JPG | PNG |
|-----------|:----:|:---:|:----:|:---:|:----:|:----:|:---:|:---:|:---:|
| **md**    | ✅ | ✅ | — | — | — | ✅ | ✅ | — | — |
| **txt**   | ✅ | ✅ | — | — | — | ✅ | — | — | — |
| **html**  | ✅ | ✅ | — | — | — | — | ✅ | — | — |
| **csv**   | ✅ | ✅ | ✅ | — | ✅ | — | — | — | — |
| **json**  | ✅ | ✅ | ✅ | ✅ | — | — | — | — | — |
| **svg**   | — | ✅ | — | — | — | — | — | ✅ | ✅ |

## Running Tests

### Python Converter Tests
Generates fixtures for all six source formats and runs every registered converter:
```bash
.venv\Scripts\python tests/test_converters.py
```

### Python Workspace Tests
Validates the temporary file lifecycle (creation, release, cleanup):
```bash
.venv\Scripts\python tests/test_workspace.py
```

### Playwright E2E Tests

Requires Node.js. Install Node dependencies and the Playwright browser binaries, then run the tests (Uvicorn starts automatically before each test run):
```bash
# Install dependencies
npm install

# Install Playwright browser binaries
npx playwright install

# Run E2E tests
npm run test:e2e            # headless
npm run test:e2e:ui         # interactive runner
npm run test:e2e:debug      # debug mode
```
