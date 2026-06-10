# Phase 2: Core Expansion Implementation - System Prompt
## Priority Converter Implementation for Adla-Badli

---

## 🎯 Phase 2 Overview

**Goal**: Expand from 2 converters to 16+ converters across all major format combinations  
**Timeline**: Structured in implementation batches for systematic delivery  
**Success Metric**: All 16+ converters tested, documented, and production-ready

This phase transforms Adla-Badli from a proof-of-concept into a comprehensive, usable file conversion tool with broad format support.

---

## 📊 Conversion Priority Matrix

### Batch 1: Text-Based Conversions (High Demand, Lower Complexity)

**Why This Batch First**:
- Document conversion is most common user need
- Pandoc is stable and well-tested
- Limited external dependencies
- Building blocks for later phases

#### Converters (8 total)
1. **Markdown → PDF** (MD→PDF)
   - Purpose: Create professional documents from markdown files
   - Approach: Pandoc → HTML → WeasyPrint
   - Key Challenge: CSS formatting and page breaks
   - Priority: CRITICAL (common workflow)

2. **Markdown → HTML** (MD→HTML)
   - Purpose: Web-ready markup export
   - Approach: Direct Pandoc conversion
   - Key Challenge: Asset embedding, relative links
   - Priority: CRITICAL (web publishing)

3. **Markdown → TXT** (MD→TXT)
   - Purpose: Plain text extraction
   - Approach: Pandoc with txt filter
   - Key Challenge: Formatting loss is expected
   - Priority: MEDIUM (less common)

4. **Text → DOCX** (TXT→DOCX)
   - Purpose: Convert plain text to formatted document
   - Approach: Parse structure, use python-docx
   - Key Challenge: Structure inference from line breaks
   - Priority: HIGH (basic document creation)

5. **Text → PDF** (TXT→PDF)
   - Purpose: Create formatted PDF from plain text
   - Approach: Pandoc to DOCX intermediate, then to PDF
   - Key Challenge: Formatting defaults
   - Priority: HIGH (document creation)

6. **Text → HTML** (TXT→HTML)
   - Purpose: Web-ready conversion of plain text
   - Approach: Parse structure, generate HTML
   - Key Challenge: Semantic markup generation
   - Priority: MEDIUM (web publishing)

7. **HTML → PDF** (HTML→PDF)
   - Purpose: Render web content as PDF
   - Approach: WeasyPrint with CSS support
   - Key Challenge: CSS handling, external resources, print styling
   - Priority: CRITICAL (web screenshots)

8. **HTML → DOCX** (HTML→DOCX)
   - Purpose: Web content as editable document
   - Approach: Parse HTML structure, rebuild in python-docx
   - Key Challenge: CSS to DOCX style mapping
   - Priority: HIGH (content preservation)

### Batch 2: Data-Centric Conversions (High Value, Medium Complexity)

**Why This Batch Second**:
- Spreadsheet/table conversions are high-value use cases
- Pandas provides powerful data normalization
- Clear schema preservation requirements
- Builds on Batch 1 infrastructure

#### Converters (8 total)
1. **JSON → XLSX** (JSON→XLSX)
   - Purpose: Convert structured data to formatted spreadsheet
   - Approach: Pandas DataFrame normalization → openpyxl formatting
   - Key Challenge: Nested structure flattening, schema detection
   - Priority: CRITICAL (data export)

2. **JSON → DOCX** (JSON→DOCX)
   - Purpose: Create formatted document from structured data
   - Approach: DataFrame → python-docx table with styling
   - Key Challenge: Nested data representation
   - Priority: MEDIUM (document generation)

3. **JSON → PDF** (JSON→PDF)
   - Purpose: Create formatted report from data
   - Approach: DataFrame → ReportLab styled table
   - Key Challenge: Pagination, large datasets
   - Priority: MEDIUM (reporting)

4. **JSON → CSV** (JSON→CSV)
   - Purpose: Flatten structured data to CSV
   - Approach: Pandas flattening → CSV export
   - Key Challenge: Nested structure handling
   - Priority: MEDIUM (data export)

5. **CSV → XLSX** (CSV→XLSX)
   - Purpose: Convert table data to formatted spreadsheet
   - Approach: Pandas → openpyxl with auto-formatting
   - Key Challenge: Type detection, column sizing
   - Priority: CRITICAL (data transformation)

6. **CSV → DOCX** (CSV→DOCX)
   - Purpose: Embed table in formatted document
   - Approach: Pandas → python-docx table
   - Key Challenge: Table formatting, pagination
   - Priority: HIGH (document generation)

7. **CSV → PDF** (CSV→PDF)
   - Purpose: Create formatted table report
   - Approach: Pandas → ReportLab styled table
   - Key Challenge: Large table handling, pagination
   - Priority: HIGH (reporting)

8. **CSV → JSON** (CSV→JSON)
   - Purpose: Convert tabular to structured data
   - Approach: Pandas with header detection → JSON structure
   - Key Challenge: Type inference, array vs object format
   - Priority: MEDIUM (data transformation)

### Batch 3: Extended Document Conversions (Medium Demand, Higher Complexity)

**Why This Batch Third**:
- HTML rendering more complex (requires Playwright/Selenium)
- Lower demand than Batches 1-2
- Builds on Batch 1 HTML support
- Image rendering adds complexity

#### Converters (5 total)
1. **HTML → TXT** (HTML→TXT)
   - Purpose: Extract text content from HTML
   - Approach: BeautifulSoup extraction → text
   - Key Challenge: Preserving structure, handling scripts
   - Priority: MEDIUM (text extraction)

2. **HTML → PNG** (HTML→PNG)
   - Purpose: Render web page as image
   - Approach: Playwright headless browser screenshot
   - Key Challenge: CSS rendering, viewport sizes, dynamic content
   - Priority: HIGH (web capture)

3. **HTML → JPEG** (HTML→JPEG)
   - Purpose: Render web page as compressed image
   - Approach: Playwright → PNG → JPEG conversion
   - Key Challenge: Quality/size balance
   - Priority: MEDIUM (web capture)

4. **SVG → PDF** (SVG→PDF)
   - Purpose: Preserve vector format in PDF
   - Approach: svglib → ReportLab PDF
   - Key Challenge: Complex SVG features, scalability
   - Priority: HIGH (vector preservation)

5. **SVG → PNG** (SVG→PNG)
   - Purpose: High-quality raster from vector
   - Approach: svglib → ReportLab → Pillow
   - Key Challenge: DPI/scaling, quality preservation
   - Priority: HIGH (vector conversion)

---

## 🔧 Implementation Structure for Phase 2

### Code Organization by Batch

**Batch 1 Directory** (`app/converters/text_converters/`)
```
text_converters/
├── __init__.py (exports all converters)
├── base_text.py (common patterns for text group)
├── markdown_to_pdf.py
├── markdown_to_html.py
├── markdown_to_txt.py
├── text_to_docx.py
├── text_to_pdf.py
├── text_to_html.py
├── html_to_pdf.py
├── html_to_docx.py
└── shared_utils.py
```

**Batch 2 Directory** (`app/converters/data_converters/`)
```
data_converters/
├── __init__.py (exports all converters)
├── base_data.py (common patterns for data group)
├── json_to_xlsx.py
├── json_to_docx.py
├── json_to_pdf.py
├── json_to_csv.py
├── csv_to_xlsx.py
├── csv_to_docx.py
├── csv_to_pdf.py
├── csv_to_json.py
└── shared_utils.py
```

**Batch 3 Directory** (`app/converters/image_converters/`)
```
image_converters/
├── __init__.py (exports all converters)
├── html_to_png.py
├── html_to_jpeg.py
├── html_to_txt.py
├── svg_to_pdf.py
├── svg_to_png.py
└── shared_utils.py
```

---

## 📋 Batch-by-Batch Implementation Workflow

### Pre-Batch Setup

**1. Shared Utilities Creation**
- Identify common patterns within batch
- Implement helper functions for:
  - Format-specific parsing
  - Common output formatting
  - Error handling patterns
  - Option validation
- Create docstrings and type hints

**2. Converter Registry Update**
- Plan registry entries for all converters in batch
- Document any dependencies or conflicts
- Update `app/converters/__init__.py` stub

**3. Test Fixture Preparation**
- Create input fixtures (simple, complex, edge-case)
- Store in `tests/fixtures/[format]/`
- Document fixture purpose
- Size fixtures for performance testing

---

## 🏗️ Individual Converter Implementation Flow

### Step 1: Converter Class Definition

**Tasks**:
- Create file with correct naming: `[source]_to_[target].py`
- Define class inheriting from `BaseConverter`
- Implement required properties (`source_extension`, `target_extension`)
- Add comprehensive docstring explaining approach
- Stub `convert()` method signature

**Documentation**:
- Explain conversion approach
- Document available options
- Note known limitations
- Reference library documentation

### Step 2: Core Conversion Logic

**Tasks**:
- Implement `convert(input_path, output_path, **kwargs)` method
- Handle main conversion workflow
- Use shared utilities from group
- Implement error handling with meaningful messages
- Add logging at key points

**Approach**:
- Parse input file according to source format
- Transform to target format using appropriate library
- Write output file to output_path
- Raise `ConversionError` on any failure

### Step 3: Option Handling

**Tasks**:
- Implement `get_metadata()` returning available options
- Document each option thoroughly
- Implement option validation
- Ensure defaults work when options omitted
- Test each option combination

**Options Definition**:
- Type (enum, int, float, string, boolean)
- Default value
- Constraints (min/max, allowed values)
- UI guidance (label, description)

### Step 4: Input Validation

**Tasks**:
- Implement `validate_input(input_path)` method
- Check file exists and readable
- Validate format-specific requirements
- Perform content validation (not just extension)
- Provide helpful error messages

**Validation Levels**:
1. File existence and accessibility
2. File format compliance
3. Content integrity
4. Format-specific constraints

### Step 5: Unit Testing

**Tasks**:
- Create `tests/test_[source]_to_[target].py`
- Write test cases for happy path
- Test each option parameter
- Test edge cases
- Test error scenarios
- Achieve >85% code coverage

**Test Categories**:
- Basic conversion (simple input → valid output)
- Option handling (each option affects output)
- Edge cases (empty, large, special characters)
- Error scenarios (corrupted, invalid, unsupported)

### Step 6: Integration Testing

**Tasks**:
- Add to group integration test file
- Test full conversion pipeline
- Test workspace management
- Test concurrent conversions
- Verify registry integration

**Test Scenarios**:
- Full HTTP request/response cycle
- File creation and cleanup
- Error response handling
- Performance within baseline

### Step 7: Performance Profiling

**Tasks**:
- Measure conversion time with standard fixtures
- Record memory usage during conversion
- Identify bottlenecks
- Compare against Phase 1 baselines
- Document findings

**Benchmarking**:
- Small file (< 1MB)
- Medium file (5-50MB)
- Large file (near limit)
- Peak memory usage

### Step 8: Documentation

**Tasks**:
- Verify docstrings are complete and accurate
- Update group README if applicable
- Update main README with new converter
- Add to API documentation
- Document any special requirements

**Documentation Updates**:
- README section for converter group
- API endpoint documentation
- Option descriptions and examples
- Known limitations
- Performance characteristics

### Step 9: Code Review Preparation

**Tasks**:
- Run linting and formatting
- Verify all tests pass
- Double-check error handling
- Review security considerations
- Prepare PR with clear description

**Review Checklist**:
- Code follows style guide
- Tests comprehensive and passing
- Documentation complete
- No security issues
- Performance acceptable

---

## 🚀 Implementation Sequence Recommendation

### Week 1-2: Batch 1 Foundation (Text Converters)

**Priority**: MD→PDF and HTML→PDF (most requested features)

1. Set up `text_converters/` structure
2. Create `shared_utils.py` with Pandoc helpers
3. Implement MD→PDF (critical path)
4. Implement HTML→PDF (complements MD→PDF)
5. Create test fixtures for text formats
6. Add unit and integration tests
7. Document and merge

**Expected Deliverables**:
- 2 production-ready converters
- Tested and documented
- Text converter infrastructure ready

### Week 2-3: Batch 1 Expansion (Remaining Text)

**Priority**: Complete text conversions for coverage

1. Implement MD→HTML and MD→TXT
2. Implement TXT→DOCX, TXT→PDF, TXT→HTML
3. Implement HTML→DOCX, HTML→TXT
4. Test cross-format compatibility
5. Performance baseline all converters

**Expected Deliverables**:
- 8 text converters complete
- All tests passing
- Performance baselines documented

### Week 3-4: Batch 2 Foundation (Data Converters)

**Priority**: JSON→XLSX and CSV→XLSX (highest value)

1. Set up `data_converters/` structure
2. Create `shared_utils.py` with Pandas helpers
3. Implement JSON→XLSX (critical for data export)
4. Implement CSV→XLSX (complements JSON handling)
5. Create test fixtures for data formats
6. Add unit and integration tests

**Expected Deliverables**:
- 2 data converters with formatting
- Schema preservation verification
- Data converter infrastructure ready

### Week 4-5: Batch 2 Expansion (Remaining Data)

**Priority**: Complete data conversions

1. Implement JSON→DOCX, JSON→PDF, JSON→CSV
2. Implement CSV→DOCX, CSV→PDF, CSV→JSON
3. Test data integrity across conversions
4. Test with large datasets
5. Performance baseline

**Expected Deliverables**:
- 8 data converters complete
- Large file handling verified
- All tests passing

### Week 5-6: Batch 3 Implementation (Advanced)

**Priority**: HTML rendering and SVG conversions

1. Set up `image_converters/` enhancements
2. Implement SVG→PDF (vector preservation)
3. Implement SVG→PNG (quality raster)
4. Implement HTML→PNG and HTML→JPEG (Playwright)
5. Implement HTML→TXT (extraction)
6. Test and validate

**Expected Deliverables**:
- 5 advanced converters
- Rendering quality verified
- Batch 3 complete

### Week 6-7: Integration and Polish

**Priority**: Complete system verification

1. Cross-batch compatibility testing
2. Performance optimization
3. Documentation completion
4. Security review
5. Final testing and validation

**Expected Deliverables**:
- 16+ converters production-ready
- Full test coverage (>85%)
- Complete documentation
- Performance baselines established

---

## 📊 Testing Throughout Phase 2

### Daily Testing Requirements

**Per Converter**:
- Unit tests for conversion logic
- Unit tests for option handling
- Unit tests for error scenarios
- Integration test with API

**Per Batch**:
- Group compatibility tests
- Cross-converter compatibility tests
- Performance baseline tests
- Concurrent conversion tests

### Continuous Integration

**Before Merge**:
- All unit tests pass
- Integration tests pass
- Linting passes
- Code coverage >85%
- Performance within baseline
- No security issues

**Post-Merge**:
- E2E tests pass
- Deployment to staging
- Manual verification
- Performance monitoring

---

## 🔒 Security Checkpoints

### Input Validation Per Batch

**Batch 1 (Text)**:
- Validate UTF-8 encoding
- Sanitize HTML before processing
- Check file size and type
- Test with malicious input

**Batch 2 (Data)**:
- Validate JSON schema compliance
- Check for injection attempts
- Validate CSV structure
- Test with large datasets

**Batch 3 (Image)**:
- Remove SVG scripts
- Validate image dimensions
- Check for resource exhaustion
- Test with complex SVG

### Error Message Security

- Don't expose file paths
- Don't expose internal stack traces
- Don't expose library versions
- Provide actionable feedback only

---

## 📈 Success Metrics for Phase 2

### Completion Criteria
- ✅ All 16+ converters implemented
- ✅ All converters tested (>85% coverage)
- ✅ All converters documented
- ✅ Performance baselines established
- ✅ Security review completed
- ✅ E2E tests passing

### Quality Metrics
- ✅ Conversion success rate >99%
- ✅ Average conversion time <30 seconds
- ✅ Error messages helpful and actionable
- ✅ No unhandled exceptions
- ✅ Memory usage stable (<500MB per conversion)

### User Experience Metrics
- ✅ All format combinations discoverable
- ✅ Options clear and functional
- ✅ Error recovery smooth
- ✅ Processing feedback provided
- ✅ Download handling reliable

---

## 🎯 Batch Dependencies and Considerations

### Batch 1 → Batch 2 Dependencies
- Text converters complete before data converters
- Shared error handling patterns established
- Test infrastructure proven
- Performance baselines set

### Batch 2 → Batch 3 Dependencies
- Document converters complete before rendering
- Pandas utilities proven
- API structure stable
- Rate limiting strategy defined

### Parallel Development Opportunities
- Batch 1 and 2 can proceed in parallel (separate teams)
- Batch 3 can start once infrastructure stable
- Documentation can be written during implementation
- Testing can begin before feature complete

---

## 📝 Handoff and Documentation

### Per Batch Handoff
- Implementation complete and tested
- Performance baselines documented
- Known limitations recorded
- Enhancement opportunities noted
- Dependencies and conflicts identified

### Phase 2 Completion Handoff
- All 16+ converters production-ready
- Comprehensive testing completed
- Full documentation available
- Performance optimization complete
- Ready for Phase 3 (Advanced Features)

---

## 🔄 Iteration and Improvement

### Post-Batch Review
- Analyze actual vs estimated timelines
- Identify recurring issues
- Update templates and tooling
- Share learnings across team

### Continuous Improvement
- Monitor error rates post-deployment
- Track user conversion patterns
- Identify optimization opportunities
- Plan Phase 3 enhancements based on usage

---

## ✨ Phase 2 Vision

By the end of Phase 2, Adla-Badli will be:

**Comprehensive**: Support all major format combinations for real-world workflows

**Reliable**: Robust error handling and validation throughout

**Fast**: Optimized conversions with clear performance characteristics

**Beautiful**: Intuitive UI showing available options and real-time feedback

**Secure**: Multi-layer validation and sanitization

**Production-Ready**: Fully tested, documented, and monitored

This phase transforms Adla-Badli from prototype to professional file conversion tool ready for real-world use.

---

**Phase 2 Document Version**: 1.0  
**Last Updated**: 2026-06-10  
**For**: Development teams implementing Phase 2 converters
