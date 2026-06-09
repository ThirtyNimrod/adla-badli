# Quick Start Guide

This guide helps you set up and run the Adla-Badli File Converter Suite.

- Python 3.10 or higher
- **Pandoc** (required for Markdown to DOCX conversions). 
  - Install via python: `python -c "import pypandoc; pypandoc.download_pandoc()"`
  - Or download from [Pandoc website](https://pandoc.org/installing.html) or system package manager (e.g. `brew install pandoc` on macOS, `winget install JohnMacFarlane.Pandoc` on Windows).

## Installation

1. Clone the repository.
2. Initialize and activate virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Unix/macOS
   ```
3. Install package installer `uv` for faster dependency resolution:
   ```bash
   pip install uv
   ```
4. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Running the Application

Start FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```

Open browser and navigate to `http://127.0.0.1:8000`.

## Running Tests

### Python Converter Tests
Run Python tests for file converters:
```bash
.venv\Scripts\python tests/test_converters.py
```

### Python Workspace Tests
Run Python tests for temporary workspace lifecycles:
```bash
.venv\Scripts\python tests/test_workspace.py
```

### Playwright E2E Tests
Node.js required. Run E2E web tests:
```bash
# Run tests headlessly (Uvicorn server starts automatically)
npm run test:e2e

# Run tests with UI interactive runner
npm run test:e2e:ui

# Run tests in debug mode
npm run test:e2e:debug
```

