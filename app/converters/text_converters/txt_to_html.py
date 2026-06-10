from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.text_converters.shared import read_source_as_html, wrap_html_document


class TxtToHtmlConverter(BaseConverter):
    """Plain text to a standalone, styled HTML document via Pandoc's markdown reader."""

    @property
    def source_extension(self) -> str:
        return "txt"

    @property
    def target_extension(self) -> str:
        return "html"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        html_body = read_source_as_html(input_path, "markdown")
        output_path.write_text(wrap_html_document(html_body, title=input_path.stem), encoding="utf-8")
