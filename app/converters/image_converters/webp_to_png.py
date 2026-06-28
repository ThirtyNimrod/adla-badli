from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from PIL import Image

from app.converters.base import BaseConverter


class WebpToPngConverter(BaseConverter):
    """WebP to PNG: decode with Pillow, save lossless with alpha preserved."""

    @property
    def source_extension(self) -> str:
        return "webp"

    @property
    def target_extension(self) -> str:
        return "png"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        with Image.open(input_path) as img:
            img.convert("RGBA").save(output_path, "PNG")
