from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.data_converters.shared import load_csv_dataframe, dataframe_to_docx


class CsvToDocxConverter(BaseConverter):
    """CSV to a Word document containing a formatted grid table."""

    @property
    def source_extension(self) -> str:
        return "csv"

    @property
    def target_extension(self) -> str:
        return "docx"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        df = load_csv_dataframe(input_path)
        dataframe_to_docx(df, output_path, title=input_path.stem)
