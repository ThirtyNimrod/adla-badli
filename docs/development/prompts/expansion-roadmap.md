# Adla-Badli Expansion Roadmap - System Prompt
## Phase 2: Universal Format Converter Suite

---

## 📈 Project Expansion Overview

**Current State**: 2 converters (MD→DOCX, SVG→JPG)  
**Target State**: 16+ converters across comprehensive AI-to-Human format coverage  
**Timeline**: Phased implementation prioritizing high-demand format pairs

This expansion transforms Adla-Badli from a basic converter into a production-ready universal format bridge, making it seamless for users and AI systems to work with any combination of technical and human-readable formats.

---

## 🎯 Complete Conversion Matrix

### Input Formats (AI-Friendly / Technical)
- **Markdown** (`.md`) — Structured text with metadata
- **Plain Text** (`.txt`) — Unformatted content
- **HTML** (`.html`) — Web-ready markup
- **CSV** (`.csv`) — Tabular data format
- **JSON** (`.json`) — Structured nested data
- **SVG** (`.svg`) — Vector graphics format

### Output Formats (Human-Friendly / Presentable)
- **DOCX** (`.docx`) — Microsoft Word documents with formatting
- **PDF** (`.pdf`) — Universal, distributed document format
- **XLSX** (`.xlsx`) — Excel spreadsheets with formatting
- **CSV** (`.csv`) — Tabular data export
- **JPEG/JPG** (`.jpg`) — Compressed raster images
- **PNG** (`.png`) — Lossless raster images

### Conversion Paths (16+ Total)

| From \ To | DOCX | PDF | XLSX | CSV | JPEG | PNG | HTML | TXT |
|-----------|------|-----|------|-----|------|-----|------|-----|
| **Markdown** | ✅ existing | ✅ new | — | ✅ new | — | — | ✅ new | ✅ new |
| **Text** | ✅ new | ✅ new | — | — | — | — | ✅ new | — |
| **HTML** | ✅ new | ✅ new | — | — | ✅ new | ✅ new | — | ✅ new |
| **CSV** | ✅ new | ✅ new | ✅ new | — | — | — | — | ✅ new |
| **JSON** | ✅ new | ✅ new | ✅ new | ✅ new | — | — | ✅ new | — |
| **SVG** | — | ✅ new | — | — | ✅ existing | ✅ new | ✅ new | — |

**Total Supported Paths**: 16+ bidirectional and unidirectional conversions

---

## 🏗️ Backend Architecture Enhancements

### Converter Organization Strategy

**Group 1: Text Format Converters (8 total)**
- Source formats: Markdown, Text, HTML
- Target formats: DOCX, PDF, HTML, TXT
- Primary approach: Pandoc-based pipeline with document formatting
- Unified handling of text-to-document conversion preserving structure and metadata
- Location: `app/converters/text_converters/`

**Group 2: Data Format Converters (8 total)**
- Source formats: CSV, JSON
- Target formats: XLSX, DOCX, PDF, CSV
- Primary approach: Pandas normalization to DataFrame, then format-specific serialization
- Handles structured data with proper table formatting and preservation of schema
- Location: `app/converters/data_converters/`

**Group 3: Image Format Converters (4 total)**
- Source format: SVG (with potential HTML rendering)
- Target formats: JPEG, PNG, PDF, HTML
- Primary approach: SVG parsing with raster/vector rendering options
- Supports quality parameters, background colors, and dimension adjustments
- Location: `app/converters/image_converters/`

### Converter Enhancement Requirements

**Registry Pattern Enhancements**
- Extend registry to support all 16+ converter pairs with clear mapping
- Implement converter discovery mechanism for dynamic listing
- Support converter-specific metadata (dependencies, performance class, requirements)
- Track converter version and deprecation status for future expansions

**Base Converter Class Enhancements**
- Add `get_metadata()` method returning available options for each converter
- Implement `validate_input()` for pre-conversion validation hooks
- Add `estimate_duration()` for progress indication
- Support converter versioning for backward compatibility

**Workspace Management Enhancements**
- Track workspace quota per user/IP for rate limiting
- Implement workspace metrics (files created, disk usage, duration)
- Support workspace archival for audit trails
- Add intelligent cleanup with configurable retention policies

### Configuration and Environment Management

**Conversion Limits**
- Maximum file size: configurable per format (default 50MB)
- Timeout per conversion type:
  - Quick: 10 seconds (SVG→PNG, small JSON→XLSX)
  - Standard: 30 seconds (MD→PDF, HTML→DOCX)
  - Extended: 60 seconds (large CSV→PDF with formatting)
- Concurrent conversion limit: configurable per IP

**Format-Specific Options**
- **Image converters**: quality (1-100), background (white/black/transparent), dimensions
- **Document converters**: page size, margins, font selection
- **Data converters**: column width auto-fit, header styling, table borders
- **HTML converters**: render mode (headless browser vs parser), CSS handling

---

## 🖥️ Frontend Enhancement Plan

### UI Component Enhancements

**Format Selection Intelligence**
- Automatic format detection from file extension
- Dynamic "To" format dropdown based on "From" selection
- Display converter metadata (time estimate, file size impact, special options)
- Format popularity indicators (cloud badge for high-demand conversions)

**Converter Options Interface**
- Dynamic option panel that renders based on selected converter
- Slider controls for numeric parameters (quality, dimensions)
- Dropdown selectors for enum options (background color, page size)
- Preview of selected options in natural language
- Tooltips explaining each option's impact

**File Handling Improvements**
- Multi-file batch conversion UI (optional, deferred to Phase 4)
- File preview before conversion (for text formats)
- Estimated conversion time display
- Storage space requirement indicator

**Progress and Feedback**
- Loading overlay with percentage or spinner
- Estimated time remaining for large conversions (>5 seconds)
- Real-time conversion status updates
- Conversion history accessible from UI

### Responsive Design Requirements
- Desktop-first layout optimized for large dropzone
- Tablet-optimized format selection panel
- Mobile-optimized with touch-friendly file picker
- All overlays and modals properly dismissible on mobile

---

## 🔄 Converter Implementation Strategy

### Text-to-Document Pipeline (Group 1)

**Markdown → DOCX/PDF/HTML/TXT**
- Use Pandoc as primary engine for consistent formatting across outputs
- Preserve heading hierarchy, lists, code blocks, and emphasis
- Handle embedded images and links appropriately
- For PDF: Use Pandoc HTML intermediate → WeasyPrint rendering

**Text → DOCX/PDF/HTML**
- Parse for basic structure (line breaks, paragraphs)
- Apply consistent basic formatting
- Optional: Infer structure from content (bulleted lists, headers)

**HTML → DOCX/PDF/TXT/PNG/JPEG**
- Parse HTML structure and CSS styling
- DOCX: Use python-docx to rebuild as structured document
- PDF: Use WeasyPrint for CSS-aware rendering
- TXT: Extract text content while preserving basic structure
- Images (PNG/JPEG): Use Playwright for full-page rendering or selected elements

### Data-to-Format Pipeline (Group 2)

**JSON → XLSX/DOCX/PDF/CSV**
- Parse JSON and normalize to pandas DataFrame
- Handle nested structures (flatten or expand appropriately)
- XLSX: Format headers with styling (bold, background), auto-fit columns, freeze panes
- DOCX: Create formatted table with alternating row colors
- PDF: Use ReportLab for styled table with proper pagination
- CSV: Simple CSV export from DataFrame

**CSV → XLSX/DOCX/PDF/JSON**
- Parse CSV into pandas DataFrame
- Preserve data types where possible
- XLSX: Add formatting, auto-adjust columns, apply table styles
- DOCX: Create formatted table with header formatting
- PDF: Page-aware table rendering with pagination
- JSON: Convert to appropriate JSON structure (array of objects, nested groups)

### Image-to-Format Pipeline (Group 3)

**SVG → PNG/JPEG/PDF/HTML**
- PNG: Use svglib → ReportLab → Pillow for quality raster conversion
- JPEG: Same as PNG plus quality parameter and background color option
- PDF: Preserve vector format using ReportLab's native SVG support
- HTML: Embed SVG directly or convert to inline data URI

### Converter Quality Standards

**Fidelity Requirements**
- Text converters: Preserve formatting, structure, and metadata
- Data converters: Preserve data integrity, row/column order, data types
- Image converters: Maintain visual quality with configurable compression

**Error Handling per Group**
- Text: Handle encoding issues, missing fonts, invalid markup
- Data: Handle malformed structures, missing values, type mismatches
- Image: Handle invalid SVG, missing assets, rendering failures

---

## 📊 API Enhancement Strategy

### Extended Converter Discovery

**GET /api/converters**
- Returns: All available converters grouped by source format
- Include: Conversion time estimates, file size multipliers, popularity scores
- Support filtering by source/target format

**GET /api/converters/:source/:target**
- Returns: Detailed converter metadata
- Include: Available options with type, constraints, defaults
- Include: Example conversions and limitations
- Include: Performance characteristics and file size estimates

### Enhanced Conversion Endpoint

**POST /api/convert**
- Accept format-specific parameters in request body
- Validate parameters against converter metadata
- Return extended response with conversion duration and statistics
- Support optional webhook callbacks for async processing

### Monitoring and Metrics Endpoint (Future)

**GET /api/metrics**
- Conversion success rate by format pair
- Average conversion times
- Popular source/target combinations
- Error rate tracking

---

## ✅ Testing and Quality Assurance Strategy

### Unit Test Coverage

**Converter Tests**
- Create comprehensive test fixtures for all input formats
- Test each converter with valid, edge-case, and invalid inputs
- Verify output file integrity and format compliance
- Validate option handling (quality, colors, dimensions)
- Test error conditions with appropriate exception handling

**Data Integrity Tests**
- Text converters: Verify no content loss, structure preservation
- Data converters: Verify row count, column mapping, data type preservation
- Image converters: Verify dimensions, format properties, quality levels

**Error Path Tests**
- Large file rejection
- Malformed input handling
- Timeout scenarios
- Resource exhaustion

### Integration Tests

**Full Pipeline Testing**
- Complete request-response cycles
- Workspace creation and cleanup verification
- Concurrent conversion handling
- Rate limiting verification

**Cross-Converter Compatibility**
- Output of one converter as input to another
- Format round-trip testing (A→B→A quality preservation)
- Multi-format document creation workflows

### E2E Test Scenarios

**User Workflows**
- Single file conversion via upload
- Drag-and-drop file handling
- Format selection and options configuration
- Download and file integrity verification
- Error recovery and retry workflows

**Performance Baselines**
- Establish baseline conversion times per format pair
- Monitor for performance regressions
- Test with various file sizes (1KB to 50MB)
- Verify temp file cleanup

---

## 🚀 Performance Optimization Approach

### Caching Strategy

**Immutable Caches**
- Converter registry (changes only on deployment)
- Available conversions list
- Converter metadata and capabilities
- Format-to-group mappings

**Request-Level Caching**
- Cache `GET /api/converters` response (15 minute TTL)
- Cache converter metadata responses
- Don't cache conversion results (user-specific)

### Async Processing

**Background Tasks**
- Workspace cleanup scheduled after response sent
- Metrics logging without blocking response
- Optional: Large file pre-processing (for future batch support)

**Timeout Management**
- Implement appropriate timeouts per conversion type
- Graceful degradation with clear error messages
- User-friendly time estimates before conversion starts

### Resource Management

**Disk Space**
- Monitor temporary directory disk usage
- Implement automated cleanup of orphaned workspaces
- Warn when disk usage approaches limits
- Configure maximum workspace age (e.g., 24 hours)

**Memory Management**
- Stream large files instead of loading into memory
- Use generators for data processing where possible
- Monitor peak memory usage during conversions
- Consider limiting concurrent conversions by resource type

---

## 🔒 Security Enhancements

### File Upload Security

**Validation Layers**
- Extension whitelist enforcement
- Magic byte validation (verify file content matches declared type)
- File size limit enforcement per format
- Optional: Virus scanning integration (ClamAV)
- Optional: Content hash tracking for duplicate detection

### Sanitization Requirements

**Format-Specific Sanitization**
- HTML: Remove/disable scripts, stylesheets targeting sensitive areas
- JSON: Validate schema, reject external references
- SVG: Remove scripts and external resources
- Documents: Disable macros and embedded executables

### Resource Limits

**Rate Limiting**
- Per-IP conversion limit (e.g., 100 per hour)
- Per-user storage quota for temporary files
- Concurrent conversion limit per IP
- File size escalation limits (prevent sudden large uploads)

### Audit and Logging

**Security Event Logging**
- Log all failed validation attempts
- Track suspicious patterns (rapid failed conversions, format spoofing)
- Optional: Record conversion metadata for audit trails
- Implement log rotation and retention policies

---

## 📈 Implementation Phases

### Phase 1: Foundation (Current)
- ✅ Registry pattern implementation
- ✅ Workspace management
- ✅ Base converter infrastructure
- ✅ 2 initial converters (MD→DOCX, SVG→JPG)

### Phase 2: Core Expansion (Priority)
- Add text converters (MD→PDF, MD→HTML, MD→TXT, TXT→DOCX, TXT→PDF, TXT→HTML)
- Add data converters (JSON→XLSX, JSON→DOCX, JSON→PDF, JSON→CSV, CSV→XLSX, CSV→DOCX, CSV→PDF, CSV→JSON)
- Enhance SVG converters (SVG→PDF, SVG→PNG)
- Extend HTML converters (HTML→PDF, HTML→DOCX, HTML→TXT, HTML→PNG, HTML→JPEG)
- Implement converter metadata system
- Add option handling to frontend

### Phase 3: Image and Rendering
- HTML screenshot converters (PNG, JPEG) with Playwright
- SVG quality enhancements
- Custom dimension and background options
- Preview functionality

### Phase 4: Advanced Features
- Batch conversion API
- Conversion templates/presets
- User conversion history
- Scheduled/delayed conversions
- Webhook notifications

### Phase 5: Production Hardening
- Comprehensive test coverage (>85%)
- Performance benchmarking and optimization
- Docker containerization
- CI/CD pipeline setup
- API documentation (OpenAPI/Swagger)
- User documentation

---

## 📋 Converter Template and Standards

### File Organization Pattern
```
app/converters/
├── [group_name]/
│   ├── __init__.py (exports converter classes)
│   ├── converter_name.py (individual converter)
│   └── shared_utils.py (group-specific helpers)
└── base.py (abstract converter)
```

### Converter Class Requirements
- Inherits from `BaseConverter`
- Implements `source_extension` property
- Implements `target_extension` property
- Implements `convert(input_path, output_path, **kwargs)` method
- Implements `get_metadata()` returning available options
- Raises `ConversionError` with meaningful messages
- Accepts format-specific options through `**kwargs`
- Includes docstring explaining approach and limitations

### Converter Registration
- Import converter in group `__init__.py`
- Register in main `app/converters/__init__.py` with tuple key `(source_ext, target_ext)`
- Update converter registry documentation

---

## 💡 Design Principles

**Modularity**: Each converter is self-contained and testable independently

**Consistency**: All converters follow same interface and error handling patterns

**Extensibility**: New converters can be added without modifying existing code

**User Experience**: Clear error messages, reasonable timeouts, predictable behavior

**Performance**: Lazy initialization, appropriate caching, resource-aware limits

**Security**: Defense in depth with multiple validation layers

**Maintainability**: Clean code structure, comprehensive documentation, automated testing

---

## 🎓 Development Standards

### Code Quality
- All converters use consistent error handling pattern
- Type hints throughout implementation
- Docstrings for public methods and classes
- Clear variable naming and function organization

### Git Workflow
- Descriptive commit messages with conventional prefixes
- One converter or feature per commit where possible
- Pull requests include unit and integration tests
- Code review before merging to main

### Documentation Requirements
- README update for new converters
- Docstring explaining conversion approach
- Known limitations and edge cases documented
- Examples of option usage in converter metadata

---

## 🎯 Success Criteria

**Completion Metrics**
- All 16+ converters implemented and tested
- >85% code coverage in unit tests
- <100ms API response time for metadata endpoints
- <30 second conversion time for 99% of requests
- Zero security vulnerabilities in file upload/handling
- Full E2E test coverage for all converter paths
- User-facing documentation complete

**Quality Gates**
- All tests passing (unit, integration, E2E)
- Linting and formatting automated
- Performance benchmarks met
- Security review completed
- Documentation reviewed

---

## 📚 Key Integration Points

**External Libraries**
- **Pandoc** (pypandoc): Core text format conversion engine
- **WeasyPrint**: HTML to PDF rendering with CSS support
- **Pillow**: Image processing and format conversion
- **svglib/cairosvg**: SVG parsing and rasterization
- **ReportLab**: Programmatic PDF and image generation
- **Pandas**: Tabular data normalization and transformation
- **openpyxl**: XLSX creation and formatting
- **python-docx**: DOCX document creation
- **BeautifulSoup/lxml**: HTML parsing and manipulation

**Frontend Dependencies**
- **Fetch API**: File upload and conversion requests
- **FormData**: Multipart form handling
- **Canvas API**: Image preview and display (optional)
- **CSS Grid/Flexbox**: Responsive layout system

---

## ✨ Vision

Adla-Badli becomes the go-to universal format converter, seamlessly bridging AI-friendly technical formats with human-readable presentable formats. The system is:

- **Comprehensive**: Supports all major format combinations
- **Reliable**: Robust error handling and validation
- **Fast**: Optimized conversions with intelligent caching
- **Secure**: Defense-in-depth security architecture
- **Beautiful**: Intuitive UI with clear user guidance
- **Extensible**: Easy to add new converters and options

This foundation enables future enhancements like batch processing, format templates, conversion history, and integration with other tools.

---

## 📝 Notes for Future Enhancement

**Potential Expansions**
- Batch conversion API and UI
- Conversion profiles/templates for common workflows
- Format conversions beyond current scope (PPTX, ODT, EPUB, TIFF)
- Image optimization filters (grayscale, compression, resizing)
- Document merging across formats
- OCR for image-to-text conversions
- Format comparison tools
- A/B testing different conversion approaches

**Monitoring and Analytics**
- Conversion success rates by format pair
- Popular conversion workflows
- Performance bottleneck identification
- User behavior analytics
- Feedback loop for optimization

**Community Features**
- User conversion templates/presets
- Community conversions library
- Format recommendations
- Conversion quality ratings

---

**Last Updated**: 2026-06-10  
**Version**: 1.0 (Expansion Roadmap)  
**Maintainer**: ThirtyNimrod
