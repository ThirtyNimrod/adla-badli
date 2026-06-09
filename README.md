# Adla-Badli File Converter Suite

FastAPI-powered file conversion tool.

## Documentation

- [Quick Start Guide](docs/quick_start.md)
- [Architecture Documentation](docs/architecture.md)

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