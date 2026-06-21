# Cross-platform Makefile for Adla-Badli File Converter Suite

ifeq ($(OS),Windows_NT)
    VENV_BIN = .venv\Scripts
    PYTHON = $(VENV_BIN)\python.exe
    PIP = $(VENV_BIN)\pip.exe
else
    VENV_BIN = .venv/bin
    PYTHON = $(VENV_BIN)/python
    PIP = $(VENV_BIN)/pip
endif

.PHONY: install serve test lint e2e clean help

help:
	@echo "Available commands:"
	@echo "  make install - Set up pip, uv, and install Python dependencies"
	@echo "  make serve   - Start the FastAPI dev server via Uvicorn"
	@echo "  make test    - Run Python unit tests"
	@echo "  make lint    - Run black, ruff, and mypy code quality checks"
	@echo "  make e2e     - Run Playwright E2E browser tests"
	@echo "  make clean   - Clean temporary test output, caches, and pycache folders"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install uv
	$(PYTHON) -m uv pip install -r requirements.txt

serve:
	$(PYTHON) -m uvicorn app.main:app --reload

test:
	$(PYTHON) tests/test_converters.py
	$(PYTHON) tests/test_workspace.py

lint:
	$(PYTHON) -m black --check .
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy app/

e2e:
	npm run test:e2e

clean:
	$(PYTHON) -c "import shutil, os; [shutil.rmtree(p, ignore_errors=True) for p in ['tests/output', '.mypy_cache', '.ruff_cache', '__pycache__']]; [os.remove(f) for f in os.listdir('.') if f.endswith('.pyc') or f.endswith('.pyo')]"
