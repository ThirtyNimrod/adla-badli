from pathlib import Path
import io
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from app.converters.base import BaseConverter

class SvgToJpgConverter(BaseConverter):
    @property
    def source_extension(self) -> str:
        return "svg"

    @property
    def target_extension(self) -> str:
        return "jpg"

    def convert(self, input_path: Path, output_path: Path) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Load and parse SVG
        drawing = svg2rlg(str(input_path))
        if drawing is None:
            raise ValueError(f"Failed to parse SVG structure from file: {input_path}")
        
        # Render SVG drawing as PNG to in-memory bytes
        png_buffer = io.BytesIO()
        renderPM.drawToFile(drawing, png_buffer, fmt="PNG")
        png_buffer.seek(0)
        
        # Open in-memory PNG with Pillow
        png_image = Image.open(png_buffer)
        
        # Create a solid white canvas to merge alpha channels (JPEG has no transparency support)
        canvas = Image.new("RGB", png_image.size, (255, 255, 255))
        
        if png_image.mode == "RGBA":
            # Paste using alpha channel as transparency mask
            canvas.paste(png_image, mask=png_image.split()[3])
        else:
            canvas.paste(png_image)
            
        # Save output image as JPEG
        canvas.save(output_path, "JPEG", quality=95)
