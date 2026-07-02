# Adla-Badli Documentation

Welcome to the documentation for the Adla-Badli File Converter Suite.

## Features & Capabilities

- **23 Conversion Paths**: Bridges Markdown, Plain Text, HTML, CSV, JSON, SVG, and WebP sources with DOCX, PDF, XLSX, CSV, JSON, HTML, TXT, JPG, and PNG targets.
- **Interactive File Previewer**: Instant inline preview rendering for images, PDFs, sandboxed HTML docs, pretty-printed JSON, text files, and CSV tables, plus stylized placeholders for Word and Excel targets.
- **Dynamic Configuration**: Form fields are dynamically populated using Pydantic option schemas.
- **Isolated Workspace**: Transparent UUID-isolated directory lifecycle with deferred background tasks for file cleanup.

## Core Documentation

- **[Quick Start Guide](core/quick_start.md)**: Steps to set up your local virtual environment, install Python and Node.js dependencies, install Playwright browsers, and start the development server.
- **[Architecture Overview](core/architecture.md)**: Deep dive into the registry pattern, workspace context manager lifecycle, layout designs, and components.
- **[Troubleshooting Guide](core/troubleshooting.md)**: Fixes for common errors, including ports in use (port 8000), Pandoc installation issues, Playwright browser failures, and Windows script execution policies.

## Development & AI Archive

- **[development/prompts/](development/prompts/)**: Prompt templates, expansion roadmaps, and guidelines used during the design phases.
