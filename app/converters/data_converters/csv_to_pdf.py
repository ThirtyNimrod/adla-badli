from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.text_converters.options import PdfOptions
from app.converters.data_converters.shared import load_csv_dataframe, dataframe_to_pdf


class CsvToPdfConverter(BaseConverter):
    """CSV to a paginated PDF table; switches to landscape for wide datasets."""

    @property
    def source_extension(self) -> str:
        return "csv"

    @property
    def target_extension(self) -> str:
        return "pdf"

    options_schema = PdfOptions

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        opts = options if isinstance(options, PdfOptions) else PdfOptions()
        df = load_csv_dataframe(input_path)
        dataframe_to_pdf(df, output_path, page_size=opts.page_size, title=input_path.stem)
