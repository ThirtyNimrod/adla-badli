from pathlib import Path
import io
import xml.etree.ElementTree as ET
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

    def convert(self, input_path: Path, output_path: Path, **kwargs) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Determine background color
        bg_option = kwargs.get("bg_color", "white").lower()
        if bg_option == "dark":
            bg_color = (11, 15, 25)  # Premium Slate (#0b0f19)
            hex_color = "#0b0f19"
            bg_int = 0x0b0f19
        elif bg_option == "black":
            bg_color = (0, 0, 0)     # Pure Black
            hex_color = "#000000"
            bg_int = 0x000000
        else:
            bg_color = (255, 255, 255) # Pure White
            hex_color = "#ffffff"
            bg_int = 0xffffff
        
        # Pre-process SVG to override background rect fill if present
        processing_path = input_path
        temp_svg_path = None
        
        try:
            ET.register_namespace('', "http://www.w3.org/2000/svg")
            tree = ET.parse(input_path)
            root = tree.getroot()
            modified = False
            
            # Find and alter any background rect
            for child in root:
                if child.tag.endswith('rect'):
                    width = child.attrib.get('width', '')
                    height = child.attrib.get('height', '')
                    # If rect is likely a background canvas
                    if '100' in width or '%' in width:
                        child.set('fill', hex_color)
                        modified = True
                        break
            
            if modified:
                temp_svg_path = input_path.parent / f"temp_{input_path.name}"
                tree.write(temp_svg_path, encoding='utf-8', xml_declaration=True)
                processing_path = temp_svg_path
        except Exception as e:
            # Fallback to original path if parsing fails
            print(f"SVG XML processing error: {e}")
            processing_path = input_path

        try:
            # Load and parse SVG
            drawing = svg2rlg(str(processing_path))
            if drawing is None:
                raise ValueError(f"Failed to parse SVG structure from file: {processing_path}")
            
            # Render SVG drawing as PNG to in-memory bytes with custom background color
            png_buffer = io.BytesIO()
            renderPM.drawToFile(drawing, png_buffer, fmt="PNG", bg=bg_int)
            png_buffer.seek(0)
        finally:
            # Clean up temp file
            if temp_svg_path and temp_svg_path.exists():
                try:
                    temp_svg_path.unlink()
                except Exception:
                    pass
        
        # Open in-memory PNG with Pillow
        png_image = Image.open(png_buffer)
        
        # Create a solid canvas with the selected background color
        canvas = Image.new("RGB", png_image.size, bg_color)
        
        if png_image.mode == "RGBA":
            # Paste using alpha channel as transparency mask
            canvas.paste(png_image, mask=png_image.split()[3])
        else:
            canvas.paste(png_image)
            
        # Save output image as JPEG
        canvas.save(output_path, "JPEG", quality=95)
