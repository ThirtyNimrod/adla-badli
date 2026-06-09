import sys
from pathlib import Path

# Add project root to python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.converters.md_to_docx import MarkdownToDocxConverter
from app.converters.svg_to_jpg import SvgToJpgConverter

def test_md_to_docx():
    print("Testing MD to DOCX...")
    input_path = project_root / "tests" / "sample.md"
    output_path = project_root / "tests" / "sample.docx"
    
    if output_path.exists():
        output_path.unlink()
        
    converter = MarkdownToDocxConverter()
    converter.convert(input_path, output_path)
    
    if output_path.exists():
        print("SUCCESS: sample.docx created successfully!")
        print(f"File size: {output_path.stat().st_size} bytes")
    else:
        print("FAILED: sample.docx was not created.")

def test_svg_to_jpg():
    print("Testing SVG to JPG...")
    input_path = project_root / "tests" / "sample.svg"
    output_path = project_root / "tests" / "sample.jpg"
    
    if output_path.exists():
        output_path.unlink()
        
    converter = SvgToJpgConverter()
    converter.convert(input_path, output_path)
    
    if output_path.exists():
        print("SUCCESS: sample.jpg created successfully!")
        print(f"File size: {output_path.stat().st_size} bytes")
    else:
        print("FAILED: sample.jpg was not created.")

if __name__ == "__main__":
    tests_dir = project_root / "tests"
    tests_dir.mkdir(exist_ok=True)
    
    # Ensure sample MD exists
    sample_md_path = tests_dir / "sample.md"
    sample_md_content = """# Test Document

This is a test of MD to DOCX conversion in **Adla-Badli**.

- Bullet point 1
- Bullet point 2

Enjoy!
"""
    with open(sample_md_path, "w", encoding="utf-8") as f:
        f.write(sample_md_content)
        
    # Ensure sample SVG exists
    sample_svg_path = tests_dir / "sample.svg"
    sample_svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="50" cy="50" r="40" fill="blue" />
</svg>"""
    with open(sample_svg_path, "w", encoding="utf-8") as f:
        f.write(sample_svg_content)
        
    test_md_to_docx()
    test_svg_to_jpg()
