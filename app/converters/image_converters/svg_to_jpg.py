from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.image_converters.shared import RasterOptions, render_svg_to_image


class SvgToJpgConverter(BaseConverter):
    """SVG to JPEG: svglib rasterization composited onto a solid background."""

    @property
    def source_extension(self) -> str:
        return "svg"

    @property
    def target_extension(self) -> str:
        return "jpg"

    options_schema = RasterOptions

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        opts = options if isinstance(options, RasterOptions) else RasterOptions()
        canvas, _ = render_svg_to_image(input_path, opts.bg_color)
        canvas.save(output_path, "JPEG", quality=95)
