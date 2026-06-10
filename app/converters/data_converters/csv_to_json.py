from pathlib import Path
from typing import Literal, Optional
from pydantic import BaseModel, Field

from app.converters.base import BaseConverter
from app.converters.data_converters.shared import load_csv_dataframe


class CsvToJsonOptions(BaseModel):
    orient: Literal["records", "columns"] = Field(
        default="records",
        title="JSON Structure",
        description="'records' produces an array of row objects; 'columns' groups values by column.",
    )


class CsvToJsonConverter(BaseConverter):
    """CSV to pretty-printed JSON, as row records or column groups."""

    @property
    def source_extension(self) -> str:
        return "csv"

    @property
    def target_extension(self) -> str:
        return "json"

    options_schema = CsvToJsonOptions

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        opts = options if isinstance(options, CsvToJsonOptions) else CsvToJsonOptions()
        df = load_csv_dataframe(input_path)
        df.to_json(output_path, orient=opts.orient, indent=2, force_ascii=False)
