from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from app.converters.base import BaseConverter
from app.converters.data_converters.shared import load_csv_dataframe

class CsvToHtmlConverter(BaseConverter):
    """CSV to styled HTML table."""

    @property
    def source_extension(self) -> str:
        return "csv"

    @property
    def target_extension(self) -> str:
        return "html"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        df = load_csv_dataframe(input_path)
        html_table = df.to_html(classes="table table-striped", index=False)
        html_doc = (
            "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n"
            "<style>\n"
            "body { font-family: sans-serif; padding: 20px; color: #333; }\n"
            "table { border-collapse: collapse; width: 100%; margin-top: 20px; }\n"
            "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n"
            "th { background-color: #f2f2f2; }\n"
            "tr:nth-child(even) { background-color: #f9f9f9; }\n"
            "</style>\n</head>\n"
            f"<body>\n<h2>Data Table ({input_path.name})</h2>\n{html_table}\n</body>\n</html>"
        )
        output_path.write_text(html_doc, encoding="utf-8")
