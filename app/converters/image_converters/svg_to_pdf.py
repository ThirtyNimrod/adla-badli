from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from reportlab.graphics import renderPDF

from app.converters.base import BaseConverter
from app.converters.image_converters.shared import load_svg_drawing


class SvgToPdfConverter(BaseConverter):
    """SVG to PDF preserving vector geometry (no rasterization)."""

    @property
    def source_extension(self) -> str:
        return "svg"

    @property
    def target_extension(self) -> str:
        return "pdf"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        drawing = load_svg_drawing(input_path)
        renderPDF.drawToFile(drawing, str(output_path))
