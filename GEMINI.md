# GEMINI.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Adla-Badli** is a full-stack file conversion suite built on FastAPI. It provides a modern web interface for converting files between multiple formats (currently Markdown→DOCX and SVG→JPG). The application runs entirely on localhost and handles all conversions locally with no external cloud dependencies.

**Key Characteristics:**
- FastAPI backend with async/await patterns
- Single-page React-like frontend using vanilla JS with drag-and-drop UI
- Modular converter architecture using a registry pattern
- Temporary file management with context managers and background cleanup
- E2E testing via Playwright with auto-server startup

## Development Commands

### Setup & Installation
```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate
# Or on Unix/macOS: source .venv/bin/activate

# Install uv for faster dependency resolution
pip install uv

# Install dependencies from requirements.txt
uv pip install -r requirements.txt
```

### Running the Application
```bash
# Start FastAPI server with auto-reload
uvicorn app.main:app --reload

# Server runs at http://127.0.0.1:8000
```

### Running Tests

**Python Converter Tests** — Unit tests for file conversion logic:
```bash
.venv\Scripts\python tests/test_converters.py
```

**Playwright E2E Tests** — Full-stack browser tests (auto-starts Uvicorn):
```bash
# Headless mode
npm run test:e2e

# Interactive UI mode (recommended for development)
npm run test:e2e:ui

# Debug mode with step-through
npm run test:e2e:debug
```

## Architecture Overview

### Backend Structure

**`app/main.py`** — FastAPI application entry point
- Routes: `GET /` (serves SPA), `GET /api/converters` (lists available conversions), `POST /api/convert` (file upload & conversion)
- Validates file extensions, looks up converters, manages temporary workspaces
- Returns converted file as download attachment with automatic cleanup via background tasks

**`app/converters/`** — Converter module architecture
- **`base.py`**: Abstract `BaseConverter` class defining the interface (`source_extension`, `target_extension`, `convert()`)
- **`__init__.py`**: Registry system mapping `(source_ext, target_ext)` tuples to converter classes; provides `get_converter()` and `list_converters()`
- **`md_to_docx.py`**: Markdown→DOCX conversion using Pandoc via pypandoc
- **`svg_to_jpg.py`**: SVG→JPG conversion using svglib + ReportLab + Pillow with support for custom background colors (white/dark/black)

**`app/workspace.py`** — Temporary file lifecycle management
- `ConversionWorkspace` context manager handles creation/cleanup of temp directories
- Implements deferred cleanup: files are released to background tasks (FastAPI `BackgroundTasks`) before response is sent
- Uses UUID-based workspace isolation to prevent collisions

### Frontend Structure

**`app/templates/index.html`** — Single HTML file with semantic markup
- Dropzone area with drag-and-drop support
- File selection and format selection controls
- Three overlays: loader (during conversion), success (with download button), error (toast notification)
- Accessibility attributes (`role`, `tabindex`, `aria-label`, `aria-live`)
- Responsive design with mobile support

**`app/static/css/style.css`** — Glassmorphism design system
- Custom CSS variables for colors, spacing, animations
- Floating gradient background elements
- Responsive grid layout

**`app/static/js/main.js`** — Vanilla JavaScript client logic
- Initializes by fetching available converters from `/api/converters`
- Drag-and-drop file handling with visual feedback
- Keyboard navigation (Space/Enter to trigger file selection)
- Form submission with `FormData` and `fetch` POST to `/api/convert`
- Manages UI state transitions (dropzone → controls → loader → success/error)
- Downloads response file using blob URL

## Design Patterns & Conventions

### Converter System
- **Registry Pattern**: All converters must inherit `BaseConverter` and implement `source_extension`, `target_extension`, `convert()`. Register via `register_converter(MyConverter)` in `__init__.py`.
- **To add a new converter**: Create a class in `app/converters/new_format.py`, inherit `BaseConverter`, implement abstract properties/methods, import and register in `__init__.py`.

### Temporary File Management
- Use `ConversionWorkspace` context manager to encapsulate file lifetime
- Call `workspace.release()` before returning response to defer cleanup to background tasks
- Cleanup callback is added to `BackgroundTasks` and executed after response is sent

### API Response Pattern
- All file conversions return `FileResponse` with the converted file as an attachment
- Error cases raise `HTTPException` with appropriate status codes and detail messages

### Frontend State Management
- DOM element IDs act as state anchors (e.g., `#loader-overlay.hidden` for visibility control)
- File selection triggers UI state transitions: `handleFileSelect()` shows controls and populates target format options
- Conversion submission uses async `fetch()` with error handling and visual feedback

## Testing Approach

### Python Tests (`tests/test_converters.py`)
- Direct instantiation of converter classes
- File I/O against sample files in `tests/` directory (sample.md, sample.svg)
- Checks for successful output file creation and file size validation
- Run with: `.venv\Scripts\python tests/test_converters.py`

### Playwright E2E Tests
- Located in `e2e/` directory (configured in `playwright.config.ts`)
- Auto-starts Uvicorn server before tests (webServer block)
- Tests browser behavior: file selection, conversion, download
- CI/CD integration via GitHub Actions (`.github/workflows/playwright.yml`)

## Adding a New File Format Conversion

1. **Create converter class** in `app/converters/format_to_format.py`:
   ```python
   from app.converters.base import BaseConverter
   
   class FormatXToFormatYConverter(BaseConverter):
       @property
       def source_extension(self) -> str:
           return "x"
       
       @property
       def target_extension(self) -> str:
           return "y"
       
       def convert(self, input_path: Path, output_path: Path, **kwargs) -> None:
           # Implementation using external library
           pass
   ```

2. **Register** in `app/converters/__init__.py`:
   ```python
   from app.converters.format_to_format import FormatXToFormatYConverter
   register_converter(FormatXToFormatYConverter)
   ```

3. **Update frontend** (`app/templates/index.html`) to show the new format in the target select dropdown (dynamically populated from `/api/converters` API, so UI updates automatically).

4. **Test** via Python tests and Playwright E2E tests.

## Dependencies

**Python (`requirements.txt`)**:
- `fastapi` — Web framework
- `uvicorn` — ASGI server
- `python-multipart` — File upload handling
- `jinja2` — HTML templating
- `pypandoc-binary` — Markdown to DOCX conversion (uses Pandoc)
- `svglib` — SVG parsing for rendering
- `reportlab` — Graphics rendering engine
- `pillow` — Image processing (JPEG output)

**Node.js (`package.json`)**:
- `@playwright/test` — E2E testing framework
- `@types/node` — TypeScript types for Node

## Key Files to Know

- `app/main.py` — All HTTP endpoints and request/response handling
- `app/converters/__init__.py` — Converter lookup and registry
- `app/workspace.py` — Temp file lifecycle and cleanup
- `app/templates/index.html` — Frontend markup (single file)
- `app/static/js/main.js` — All client-side logic
- `tests/test_converters.py` — Converter unit tests
- `docs/architecture.md` — Extended architecture diagrams and details
