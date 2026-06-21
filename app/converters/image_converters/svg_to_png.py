from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from app.converters.base import BaseConverter
from app.converters.image_converters.shared import PngOptions, render_svg_to_image


class SvgToPngConverter(BaseConverter):
    """SVG to PNG: same rasterization pipeline as JPEG, saved lossless."""

    @property
    def source_extension(self) -> str:
        return "svg"

    @property
    def target_extension(self) -> str:
        return "png"

    options_schema = PngOptions

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        opts = options if isinstance(options, PngOptions) else PngOptions()
        canvas, _ = render_svg_to_image(input_path, opts.bg_color, dpi=opts.dpi)
        canvas.save(output_path, "PNG", compress_level=opts.compression)
