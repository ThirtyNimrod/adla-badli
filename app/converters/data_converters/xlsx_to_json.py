from pathlib import Path
from typing import Optional
from pydantic import BaseModel
import pandas as pd
from app.converters.base import BaseConverter

class XlsxToJsonConverter(BaseConverter):
    """Excel (XLSX) to JSON."""

    @property
    def source_extension(self) -> str:
        return "xlsx"

    @property
    def target_extension(self) -> str:
        return "json"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        df = pd.read_excel(input_path, engine="openpyxl", dtype=object, keep_default_na=False)
        df.to_json(output_path, orient="records", indent=2, force_ascii=False)
