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
   You can install using the Makefile shortcut:
   ```bash
   make install
   ```
   Or manually:
   ```bash
   pip install uv
   uv pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI application via the Makefile command:
```bash
make serve
```
Or manually:
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

## Development & Verification Commands

You can run quality checks, unit tests, and E2E browser tests using the Makefile targets:

- **Linting & Type Checking**: Runs Black formatter check, Ruff linter check, and Mypy static type checking:
  ```bash
  make lint
  ```
- **Python Unit Tests**: Runs the converter test suite (including option schema checks, parameterized options validation, and edge case tests) and workspace lifecycle tests:
  ```bash
  make test
  ```
- **Playwright E2E Browser Tests**: Runs the frontend end-to-end tests (auto-starting the development server):
  ```bash
  make e2e
  ```
- **Clean Temporary Files & Cache**: Deletes outputs, Pycache files, and Ruff/Mypy directories:
  ```bash
  make clean
  ```
