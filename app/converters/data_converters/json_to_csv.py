from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.data_converters.shared import load_json_dataframe


class JsonToCsvConverter(BaseConverter):
    """JSON to CSV: nested records are flattened into dotted column names."""

    @property
    def source_extension(self) -> str:
        return "json"

    @property
    def target_extension(self) -> str:
        return "csv"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        df = load_json_dataframe(input_path)
        df.to_csv(output_path, index=False, encoding="utf-8")
