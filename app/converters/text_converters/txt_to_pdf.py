from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.text_converters.options import PdfOptions
from app.converters.text_converters.shared import read_source_as_html, html_to_pdf_file


class TxtToPdfConverter(BaseConverter):
    """Plain text to PDF: markdown reader for structure, xhtml2pdf for rendering."""

    @property
    def source_extension(self) -> str:
        return "txt"

    @property
    def target_extension(self) -> str:
        return "pdf"

    options_schema = PdfOptions

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        opts = options if isinstance(options, PdfOptions) else PdfOptions()
        html_body = read_source_as_html(input_path, "markdown")
        html_to_pdf_file(
            html_body, 
            output_path, 
            page_size=opts.page_size, 
            title=input_path.stem, 
            font_size=opts.font_size, 
            margin=opts.margin
        )
