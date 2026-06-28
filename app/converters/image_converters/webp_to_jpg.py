from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from PIL import Image

from app.converters.base import BaseConverter


class WebpToJpgConverter(BaseConverter):
    """WebP to JPEG: decode with Pillow, flatten to RGB, save at quality 95."""

    @property
    def source_extension(self) -> str:
        return "webp"

    @property
    def target_extension(self) -> str:
        return "jpg"

    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        with Image.open(input_path) as img:
            rgba = img.convert("RGBA")
            canvas = Image.new("RGB", rgba.size, (255, 255, 255))
            canvas.paste(rgba, mask=rgba.split()[3])
            canvas.save(output_path, "JPEG", quality=95)
