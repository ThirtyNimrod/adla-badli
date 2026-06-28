"""Image converter group: SVG and WebP sources rendered to raster/vector targets."""
from app.converters.image_converters.svg_to_jpg import SvgToJpgConverter
from app.converters.image_converters.svg_to_png import SvgToPngConverter
from app.converters.image_converters.svg_to_pdf import SvgToPdfConverter
from app.converters.image_converters.webp_to_png import WebpToPngConverter
from app.converters.image_converters.webp_to_jpg import WebpToJpgConverter

IMAGE_CONVERTERS = [
    SvgToJpgConverter,
    SvgToPngConverter,
    SvgToPdfConverter,
    WebpToPngConverter,
    WebpToJpgConverter,
]
