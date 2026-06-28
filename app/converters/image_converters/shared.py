"""Shared helpers for the image converter group (svg sources).

For raster targets, SVGs are rasterized to PNG bytes with cairosvg (primary)
or Wand/ImageMagick (fallback), then finished with Pillow (background
compositing, encoding). For PDF, svglib parses the SVG into a ReportLab
drawing that renderPDF emits as vector geometry.
"""
import io
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Literal, Tuple

from PIL import Image
from pydantic import BaseModel, Field
from svglib.svglib import svg2rlg

BgColor = Literal["white", "dark", "black"]

# Named background palette: (rgb tuple, hex string, packed int)
_BACKGROUNDS = {
    "white": ((255, 255, 255), "#ffffff", 0xFFFFFF),
    "dark": ((11, 15, 25), "#0b0f19", 0x0B0F19),   # premium slate
    "black": ((0, 0, 0), "#000000", 0x000000),
}


class RasterOptions(BaseModel):
    bg_color: BgColor = Field(
        default="white",
        title="Background Color",
        description="Canvas color composited behind transparent SVG regions.",
    )


def load_svg_drawing(input_path: Path):
    """Parses an SVG file into a ReportLab drawing for vector output (PDF)."""
    drawing = svg2rlg(str(input_path))
    if drawing is None:
        raise ValueError(f"Failed to parse SVG structure from file: {input_path}")
    return drawing


def render_svg_to_image(input_path: Path, bg_option: BgColor = "white") -> Tuple[Image.Image, Tuple[int, int, int]]:
    """Rasterizes an SVG onto a solid background canvas.

    Returns the composited RGB Pillow image and the background color used.
    Full-canvas background rects inside the SVG are recolored to match the
    requested background so the canvas reads as one continuous surface.
    """
    bg_rgb, bg_hex, bg_int = _BACKGROUNDS[bg_option]

    processing_path = _override_background_rect(input_path, bg_hex)
    try:
        png_bytes = _svg_to_png_bytes(processing_path)
    finally:
        if processing_path != input_path and processing_path.exists():
            try:
                processing_path.unlink()
            except OSError:
                pass

    png_image = Image.open(io.BytesIO(png_bytes))
    canvas = Image.new("RGB", png_image.size, bg_rgb)
    if png_image.mode == "RGBA":
        canvas.paste(png_image, mask=png_image.split()[3])
    else:
        canvas.paste(png_image)
    return canvas, bg_rgb


def _svg_to_png_bytes(svg_path: Path) -> bytes:
    """Rasterizes an SVG file to PNG bytes.

    Uses cairosvg when available, falling back to Wand (ImageMagick). The PNG
    is rendered with transparency so the caller can composite it onto a solid
    background of its choosing.
    """
    try:
        import cairosvg

        return cairosvg.svg2png(url=str(svg_path))
    except Exception as cairo_exc:
        try:
            from wand.image import Image as WandImage
        except ImportError as wand_exc:
            raise RuntimeError(
                "SVG rasterization requires either cairosvg or Wand (ImageMagick). "
                f"cairosvg failed ({cairo_exc}); Wand is not installed ({wand_exc})."
            ) from cairo_exc

        with WandImage(filename=str(svg_path)) as wand_img:
            wand_img.format = "png"
            return wand_img.make_blob()


def _override_background_rect(input_path: Path, bg_hex: str) -> Path:
    """Rewrites a likely full-canvas <rect> fill to the requested background.

    Returns a temp SVG path when a rewrite happened, otherwise the original path.
    """
    try:
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        tree = ET.parse(input_path)
        root = tree.getroot()
        for child in root:
            if child.tag.endswith("rect"):
                width = child.attrib.get("width", "")
                if "100" in width or "%" in width:
                    child.set("fill", bg_hex)
                    temp_path = input_path.parent / f"temp_{input_path.name}"
                    tree.write(temp_path, encoding="utf-8", xml_declaration=True)
                    return temp_path
    except ET.ParseError:
        pass
    return input_path
