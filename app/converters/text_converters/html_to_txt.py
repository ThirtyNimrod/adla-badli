from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.text_converters.shared import convert_to_plain_text


class HtmlToTxtConverter(BaseConverter):
    """HTML to readable plain text via Pandoc's plain writer (tags stripped)."""

    @property
    def source_extension(self) -> str:
        return "html"

    @property
    def target_extension(self) -> str:
        return "txt"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        convert_to_plain_text(input_path, output_path, "html")
