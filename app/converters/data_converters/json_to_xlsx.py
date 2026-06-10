from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.data_converters.shared import load_json_dataframe, dataframe_to_xlsx


class JsonToXlsxConverter(BaseConverter):
    """JSON to a styled Excel workbook: flattens records, formats the header row."""

    @property
    def source_extension(self) -> str:
        return "json"

    @property
    def target_extension(self) -> str:
        return "xlsx"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        df = load_json_dataframe(input_path)
        dataframe_to_xlsx(df, output_path, sheet_name=input_path.stem[:31] or "Data")
