from pathlib import Path
from typing import Optional
from pydantic import BaseModel
import pandas as pd
from app.converters.base import BaseConverter

class XlsxToCsvConverter(BaseConverter):
    """Excel (XLSX) to CSV."""

    @property
    def source_extension(self) -> str:
        return "xlsx"

    @property
    def target_extension(self) -> str:
        return "csv"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        # Read excel first sheet using openpyxl engine
        df = pd.read_excel(input_path, engine="openpyxl", dtype=object, keep_default_na=False)
        df.to_csv(output_path, index=False, encoding="utf-8")
