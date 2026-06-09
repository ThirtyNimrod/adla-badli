from typing import Dict, Tuple, Type, List
from app.converters.base import BaseConverter
from app.converters.md_to_docx import MarkdownToDocxConverter
from app.converters.svg_to_jpg import SvgToJpgConverter

# Converter Registry mapping (source_ext, target_ext) -> Class
_REGISTRY: Dict[Tuple[str, str], Type[BaseConverter]] = {}

def register_converter(converter_cls: Type[BaseConverter]) -> None:
    """Registers a converter class in the application registry."""
    instance = converter_cls()
    key = (instance.source_extension.lower().lstrip('.'), instance.target_extension.lower().lstrip('.'))
    _REGISTRY[key] = converter_cls

# Register default converters
register_converter(MarkdownToDocxConverter)
register_converter(SvgToJpgConverter)

def get_converter(source_ext: str, target_ext: str) -> BaseConverter:
    """
    Retrieves an instance of the converter for the given extensions.
    Raises ValueError if no converter matches.
    """
    key = (source_ext.lower().lstrip('.'), target_ext.lower().lstrip('.'))
    converter_cls = _REGISTRY.get(key)
    if not converter_cls:
        raise ValueError(f"No converter registered for .{source_ext} to .{target_ext}")
    return converter_cls()

def list_converters() -> List[Dict[str, str]]:
    """
    Lists all available conversions.
    """
    return [
        {"source": key[0], "target": key[1]}
        for key in _REGISTRY.keys()
    ]
