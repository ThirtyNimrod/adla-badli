# Converter Group Implementation Template - System Prompt
## Guidelines for Adding New Converter Groups and Formats

---

## 📌 Overview

This template provides a systematic approach for implementing a new converter group or individual converters within Adla-Badli. It ensures consistency, quality, and maintainability across all converters while remaining flexible for format-specific optimizations.

---

## 🎯 Pre-Implementation Checklist

Before starting development on a new converter or converter group, complete the following:

### Format Research
- [ ] Understand the source format specification (parsing requirements, edge cases)
- [ ] Understand target format specification (constraints, formatting options)
- [ ] Identify best-in-class libraries for conversion (evaluate alternatives)
- [ ] Document conversion approach and any limitations
- [ ] Identify potential data loss scenarios (structure, formatting, metadata)

### Integration Planning
- [ ] Determine which converter group the conversion belongs to
- [ ] Check if conversion already exists in registry
- [ ] Identify file size and performance constraints
- [ ] Plan error handling strategy specific to format pair
- [ ] Document any external dependencies or system requirements

### Test Strategy
- [ ] Identify test fixtures needed (valid, edge-case, invalid inputs)
- [ ] Plan expected output validation approach
- [ ] Identify performance baselines for sizing conversions
- [ ] Plan error scenario testing

---

## 🏗️ Converter Implementation Structure

### Directory Organization
```
app/converters/
├── [group_name]/
│   ├── __init__.py
│   ├── converter_1.py
│   ├── converter_2.py
│   └── shared_utils.py (if needed)
└── base.py
```

**Group Naming Convention**: Use plural form of source format (e.g., `text_converters`, `data_converters`, `image_converters`)

### File Naming Convention
- Converter file: `[source_format]_to_[target_format].py`
- Class name: `[SourceCaps]To[TargetCaps]Converter`
- Example: `markdown_to_pdf.py` → `MarkdownToPdfConverter`

---

## 💻 Converter Class Structure

### Required Components

**1. Properties**
- `source_extension`: Property returning lowercase extension without dot (e.g., `"md"`)
- `target_extension`: Property returning lowercase extension without dot (e.g., `"pdf"`)

**2. Core Methods**
- `convert(input_path, output_path, **kwargs)`: Main conversion method
  - Takes: Path to input file, path for output file, optional parameters
  - Returns: None on success
  - Raises: `ConversionError` with descriptive message on failure

**3. Optional Methods**
- `get_metadata()`: Returns dict with available conversion options
  - Format: `{"options": [{"name": str, "type": str, "default": any, "constraints": dict}]}`
  - Example options: `quality` (int, 1-100), `background` (enum), `page_size` (enum)

- `validate_input(input_path)`: Pre-conversion validation hook
  - Checks file integrity, content validity, specific format requirements
  - Returns: None on success
  - Raises: `InvalidFileError` with specific problem description

- `estimate_duration()`: Returns estimated conversion time in seconds
  - Used for progress indication in UI
  - Conservative estimate (bias toward longer)

### Docstring Requirements
- One-line summary of conversion approach
- Explanation of how source is parsed and target is generated
- Known limitations and edge cases
- Any special parameters or requirements
- Example: Pandoc-based conversion, WeasyPrint rendering for PDF, etc.

### Error Handling Pattern
```
On failure, raise ConversionError with:
- message: Human-readable description of what failed
- error_code: Machine-readable code (e.g., "pdf_rendering_failed")
- cause: Original exception (preserved in logs)
```

---

## 📊 Group-Specific Implementation Patterns

### Text Converter Group Pattern

**What It Handles**: MD, TXT, HTML → DOCX, PDF, HTML, TXT

**Primary Approach**:
- Pandoc as primary conversion engine for text-based formats
- WeasyPrint for HTML-to-PDF rendering with CSS support
- BeautifulSoup/lxml for HTML parsing when needed

**Shared Utilities** (`text_converters/shared_utils.py`):
- Pandoc command builder with common options
- HTML sanitization and validation
- Text extraction and structure detection
- Common CSS templates for formatting

**Format-Specific Considerations**:
- **Markdown**: Preserve heading hierarchy, code blocks, emphasis, links
- **Plain Text**: Infer structure from content (line breaks, lists), apply consistent formatting
- **HTML**: Handle CSS styling, embedded resources, malformed markup
- **DOCX**: Preserve section structure, maintain formatting consistency
- **PDF**: Use CSS for layout, handle pagination properly
- **HTML output**: Ensure valid markup, handle special characters

**Option Parameters**:
- Page size (letter, A4)
- Margins (top, bottom, left, right)
- Font selection (serif, sans-serif)
- Line spacing (single, 1.5, double)
- Heading styles (level mapping)

### Data Converter Group Pattern

**What It Handles**: CSV, JSON → XLSX, DOCX, PDF, CSV, JSON

**Primary Approach**:
- Pandas for data normalization to DataFrame
- Format-specific serialization (openpyxl, python-docx, reportlab)
- Intelligent data type detection and preservation

**Shared Utilities** (`data_converters/shared_utils.py`):
- CSV parsing with encoding detection
- JSON structure normalization (flatten, expand, etc.)
- DataFrame to various output formats
- Table styling and formatting
- Column width auto-calculation
- Header detection and styling

**Format-Specific Considerations**:
- **CSV**: Handle delimiters, quoted fields, missing values, encoding
- **JSON**: Normalize nested structures, handle arrays vs objects, preserve schema
- **XLSX**: Format headers, auto-fit columns, apply table styles, freeze panes
- **DOCX**: Create formatted tables with alternating row colors, headers
- **PDF**: Handle pagination, table sizing, maintain readability

**Option Parameters**:
- Header row detection (auto, row number, none)
- Delimiter selection (for CSV)
- Column width mode (auto-fit, fixed, percentage)
- Header styling (bold, background color, font)
- Alternating row colors
- Table borders (thin, medium, thick, none)
- Number formatting (decimal places, currency, percentage)

### Image Converter Group Pattern

**What It Handles**: SVG → PNG, JPEG, PDF, HTML

**Primary Approach**:
- svglib for SVG parsing
- ReportLab for rendering
- Pillow for image output and options handling
- Playwright for HTML rendering (if needed)

**Shared Utilities** (`image_converters/shared_utils.py`):
- SVG validation and parsing
- DPI and scaling calculations
- Background color handling
- Image compression and quality settings
- Dimension calculations and resizing

**Format-Specific Considerations**:
- **SVG**: Parse without executing scripts, handle missing assets, preserve vector quality
- **PNG**: Lossless output, support transparency, handle background
- **JPEG**: Lossy compression, background blending, quality control
- **PDF**: Preserve vectors, support embedding, handle scaling

**Option Parameters**:
- Quality (1-100 for JPEG)
- Background color (white, black, transparent)
- Custom width/height
- DPI/scaling factor
- Preserve aspect ratio
- Compression level (for PNG)

---

## 🧪 Testing Pattern

### Unit Test Structure

**Test File Location**: `tests/converters/test_[group]_[converter].py`

**Test Setup**:
```
- Create test fixtures (valid, edge-case, invalid input files)
- Set up temporary directories for output
- Initialize converter instance
- Capture any logging/warnings
```

**Core Test Cases**:
1. **Happy Path**: Valid input → Valid output
   - Input fixture with standard format
   - Verify output file exists and has size > 0
   - Verify output format matches expected type
   - Spot-check output content integrity

2. **Option Handling**: Test each available option
   - Each option parameter generates expected variation
   - Default option used when not specified
   - Invalid option values handled gracefully

3. **Edge Cases**:
   - Empty input (0 bytes file)
   - Large input (test size limits)
   - Special characters in content
   - Unsupported features (e.g., SVG scripts)
   - Missing optional resources (fonts, assets)
   - Malformed input (corrupted files)

4. **Error Scenarios**:
   - Invalid input file (wrong format)
   - Corrupted file content
   - Missing required fields/structure
   - Insufficient resources
   - Timeout conditions
   - Expected exceptions raised with correct error codes

### Integration Test Structure

**Test File Location**: `tests/converters/test_[group]_integration.py`

**Test Scenarios**:
1. **Full Conversion Pipeline**: File upload → conversion → download
2. **Registry Integration**: Verify converter registered and discoverable
3. **Workspace Management**: Temp files created and cleaned
4. **Concurrent Conversions**: Multiple conversions simultaneously
5. **Error Recovery**: Failed conversion doesn't affect subsequent ones

### Test Fixture Strategy

**Fixture Organization**: `tests/fixtures/input_formats/`
```
tests/fixtures/
├── markdown/
│   ├── simple.md
│   ├── complex.md (with code, tables, links, images)
│   └── edge_cases.md (special chars, unicode)
├── json/
│   ├── simple.json (flat array of objects)
│   ├── complex.json (nested structures)
│   └── edge_cases.json (nulls, empty arrays, large numbers)
├── csv/
│   ├── simple.csv
│   ├── complex.csv (quoted fields, delimiters in data)
│   └── edge_cases.csv (missing values, encoding)
└── ...
```

**Fixture Quality Standards**:
- Real-world examples (not contrived)
- Cover expected usage patterns
- Include content that exercises specific features
- Document what each fixture tests

---

## 📋 Option/Parameter Design

### Standard Option Format
Each option in `get_metadata()` should include:
- `name`: Identifier for programmatic use (snake_case)
- `label`: Human-readable name for UI display
- `type`: Option type (enum, int, float, string, boolean)
- `description`: What the option does
- `default`: Default value if not specified
- `constraints`: Format-specific limits
  - For int/float: `{"min": N, "max": M, "step": S}`
  - For enum: `{"values": [list of options]}`
  - For string: `{"pattern": regex, "max_length": N}`

### Common Parameters Across Groups

**Quality/Compression**
- Used by: Image converters, PDF converters
- Type: integer
- Range: 1-100
- Default: 85
- UI: Slider
- Impact: File size vs visual quality tradeoff

**Background Color**
- Used by: Image converters
- Type: enum
- Values: ["white", "black", "transparent"]
- Default: "white"
- UI: Color picker or dropdown
- Impact: SVG/HTML rendering background

**Page Size**
- Used by: Document converters
- Type: enum
- Values: ["letter", "a4", "legal"]
- Default: "letter"
- UI: Dropdown
- Impact: Document dimensions

**Dimensions (Width/Height)**
- Used by: Image/HTML converters
- Type: integer (pixels or percentage)
- Constraints: Min reasonable size, max reasonable size
- Default: Auto/original size
- UI: Number input or slider
- Impact: Output dimensions

---

## 🔍 Validation and Error Handling

### Input Validation Hierarchy

1. **File Existence**: Does input file exist?
2. **File Size**: Is it within limits?
3. **File Extension**: Does it match expected format?
4. **File Content**: Can it be parsed/understood?
5. **Converter-Specific**: Format-specific validation (e.g., valid JSON schema)

### Error Message Guidelines

**Good Error Messages**:
- Specific: Identify exact problem (not just "conversion failed")
- Actionable: User can understand what to fix
- Recoverable: Indicate if user can retry with different input/options
- Contextual: Include relevant file info (name, size, format)

**Example**: 
- ❌ "Conversion failed"
- ✅ "JSON file contains invalid UTF-8 encoding at line 42. Please ensure file is UTF-8 encoded."

### Error Codes Pattern

Use machine-readable error codes for programmatic handling:
- `invalid_input_format`: File format not recognized
- `conversion_failed`: Conversion engine error
- `timeout`: Conversion exceeded time limit
- `insufficient_resources`: Memory/disk space issues
- `unsupported_feature`: Format feature not supported in target

---

## 📈 Performance Considerations

### Performance Profiling

**Before Optimization**:
- Measure baseline conversion time with standard fixtures
- Identify bottlenecks (parsing, rendering, I/O, serialization)
- Profile memory usage

**Optimization Approach**:
- Stream processing for large files
- Lazy loading of resources
- Caching intermediate results
- Batch processing where possible

### Performance Targets

**Quick Conversions** (< 5 seconds):
- SVG → PNG/JPEG (small files)
- CSV → XLSX (< 10K rows)
- JSON → XLSX (< 10K rows)
- Small markdown → PDF

**Standard Conversions** (5-30 seconds):
- Large CSV/JSON → document formats
- HTML → PDF with complex CSS
- Large markdown → PDF

**Extended Conversions** (30-60 seconds):
- Very large data exports (> 100K rows)
- Complex HTML rendering to images
- Batch operations (future feature)

### Resource Limits

**Memory**:
- Single converter shouldn't exceed 500MB
- Peak usage during largest typical conversion
- Profile with largest expected files

**Disk**:
- Temporary files cleaned after response
- Monitor disk usage growth
- Implement aggressive cleanup if needed

**Time**:
- Enforce timeout based on conversion type
- Provide user feedback for operations > 5 seconds
- Consider async processing for very long operations

---

## 🔒 Security in Converters

### Input Sanitization

**Text-Based Formats**:
- Remove/disable scripts from HTML before processing
- Validate UTF-8 encoding
- Reject files with suspicious byte patterns

**Data Formats**:
- Validate JSON schema
- Reject overly nested structures (DoS protection)
- Limit array sizes

**Image Formats**:
- Remove script content from SVG
- Disable external resource loading
- Validate dimensions (prevent resource exhaustion)

### Safe File Handling

- Always write to workspace, never overwrite source
- Use UUID-based naming to prevent collisions
- Validate output file before returning
- Clean up all temporary files

### External Library Considerations

- Keep all libraries up to date
- Review security advisories regularly
- Use subprocess with proper argument escaping
- Don't execute user content

---

## 📚 Documentation Requirements

### Converter Docstring Template

```
Brief one-line description of conversion approach.

Extended description explaining:
- How source format is parsed
- How target format is generated
- Key approach (library, algorithm, etc.)
- Data preservation/loss expectations
- Performance characteristics
- Known limitations

Available Options:
- [option_name]: Description and impact

Supported Features:
- Feature 1
- Feature 2

Known Limitations:
- Limitation 1 (workaround if applicable)
- Limitation 2
```

### README Updates

For each new converter group, update main README with:
- Converter purpose and use cases
- Supported source/target combinations
- Available options and their effects
- Performance expectations
- Known limitations
- Example usage

### API Documentation

Update OpenAPI/Swagger specs with:
- Endpoint descriptions
- Request/response schemas
- Option parameter definitions
- Example requests/responses
- Error code documentation

---

## 🚀 Deployment Checklist

Before marking a converter as production-ready:

### Code Quality
- [ ] All code passes linting (ESLint/Pylint)
- [ ] Type hints throughout (Python)
- [ ] Docstrings complete and accurate
- [ ] No hardcoded values or paths

### Testing
- [ ] Unit tests for all code paths (>85% coverage)
- [ ] Integration tests for converter group
- [ ] E2E tests for full workflow
- [ ] Performance baseline established
- [ ] All tests passing in CI/CD

### Security
- [ ] Input validation comprehensive
- [ ] File sanitization implemented
- [ ] Error messages don't leak internal info
- [ ] Security review completed

### Documentation
- [ ] Docstrings match implementation
- [ ] README updated
- [ ] API docs updated
- [ ] Known limitations documented

### Performance
- [ ] Baseline conversion times met
- [ ] Memory usage within limits
- [ ] No memory leaks identified
- [ ] Temp files cleaned properly

---

## 🔄 Future Enhancement Hooks

### Extensibility Points

**Option Expansion**: Format options can be extended without breaking existing code
- New options automatically appear in UI
- Default values ensure backward compatibility

**Library Upgrades**: Conversion approaches can be swapped
- Alternative libraries can replace primary approach
- Interface remains constant

**Performance Optimization**: Bottlenecks identified for future improvement
- Caching strategies can be added
- Parallel processing can be implemented
- Streaming can replace batch processing

### Version Management

When making breaking changes:
- Bump converter version in metadata
- Maintain deprecated converters temporarily
- Provide migration path for users
- Document in changelog

---

## 📊 Monitoring and Observability

### Metrics to Track

**Per Converter**:
- Success/failure rate
- Average duration
- File size distribution
- Error code frequency
- Peak concurrent usage

**Group Level**:
- Total conversions per group
- Group-wide success rate
- Most/least popular converters
- Resource usage patterns

### Logging Requirements

Log at conversion completion:
- Timestamp (ISO 8601)
- Source/target formats
- Input/output file size
- Duration (seconds)
- Success/failure status
- Error code (if failed)
- User/session identifier (if applicable)

### Health Checks

Implement health monitoring:
- Library availability (Pandoc, WeasyPrint, etc.)
- Disk space for temp files
- Memory availability
- Response time baselines

---

## ✨ Continuous Improvement

### Feedback Loops

**User Feedback**:
- Track failed conversions by type
- Monitor support requests
- Collect user conversion preferences
- Identify missing features

**Performance Monitoring**:
- Identify slow converter pairs
- Monitor for regressions
- Track resource usage trends
- Alert on anomalies

**Quality Improvements**:
- Regular review of error rates
- Update fixtures from real-world usage
- Optimize based on actual usage patterns
- Deprecate unused converters

---

## 📝 Notes for Implementers

**Start with tests**: Write test cases before implementation

**Use fixtures**: Real-world examples improve quality

**Document as you go**: Docstrings written during development catch issues

**Performance first**: Profile early to avoid surprises late

**Security always**: Input validation isn't optional

**Error handling matters**: Users value clear error messages

**Keep it simple**: Don't over-engineer for hypothetical features

---

**Template Version**: 1.0  
**Last Updated**: 2026-06-10  
**Applicable To**: All new converter implementations
