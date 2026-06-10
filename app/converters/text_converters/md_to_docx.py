from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.text_converters.shared import convert_via_pandoc


class MarkdownToDocxConverter(BaseConverter):
    """Markdown to DOCX via Pandoc, mapping markdown structure to Word styles."""

    @property
    def source_extension(self) -> str:
        return "md"

    @property
    def target_extension(self) -> str:
        return "docx"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        convert_via_pandoc(input_path, output_path, source_format="markdown", target_format="docx")
