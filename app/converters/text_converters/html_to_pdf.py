from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.text_converters.options import PdfOptions
from app.converters.text_converters.shared import read_source_as_html, html_to_pdf_file


class HtmlToPdfConverter(BaseConverter):
    """HTML to PDF, normalized through Pandoc then rendered with xhtml2pdf.

    The Pandoc pass strips scripts and normalizes malformed markup before
    rendering. Complex CSS layouts are simplified to document flow.
    """

    @property
    def source_extension(self) -> str:
        return "html"

    @property
    def target_extension(self) -> str:
        return "pdf"

    options_schema = PdfOptions

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        opts = options if isinstance(options, PdfOptions) else PdfOptions()
        html_body = read_source_as_html(input_path, "html")
        html_to_pdf_file(html_body, output_path, page_size=opts.page_size, title=input_path.stem)
