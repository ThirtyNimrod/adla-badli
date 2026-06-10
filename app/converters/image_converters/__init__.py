"""Image converter group: SVG sources rendered to raster and vector targets."""
from app.converters.image_converters.svg_to_jpg import SvgToJpgConverter
from app.converters.image_converters.svg_to_png import SvgToPngConverter
from app.converters.image_converters.svg_to_pdf import SvgToPdfConverter

IMAGE_CONVERTERS = [
    SvgToJpgConverter,
    SvgToPngConverter,
    SvgToPdfConverter,
]
