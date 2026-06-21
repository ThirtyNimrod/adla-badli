from pathlib import Path
from typing import Optional
from pydantic import BaseModel
import pdfplumber
from app.converters.base import BaseConverter

class PdfToTxtConverter(BaseConverter):
    """PDF to Plain Text using pdfplumber."""

    @property
    def source_extension(self) -> str:
        return "pdf"

    @property
    def target_extension(self) -> str:
        return "txt"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        text_content = []
        with pdfplumber.open(input_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
                    
        full_text = "\n\n--- Page Break ---\n\n".join(text_content)
        output_path.write_text(full_text, encoding="utf-8")
