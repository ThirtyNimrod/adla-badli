from typing import Dict, Tuple, Type, List, Any
from app.converters.base import BaseConverter
from app.converters.text_converters import TEXT_CONVERTERS
from app.converters.data_converters import DATA_CONVERTERS
from app.converters.image_converters import IMAGE_CONVERTERS

# Converter Registry mapping (source_ext, target_ext) -> Class
_REGISTRY: Dict[Tuple[str, str], Type[BaseConverter]] = {}

def register_converter(converter_cls: Type[BaseConverter]) -> None:
    """Registers a converter class in the application registry."""
    instance = converter_cls()
    key = (instance.source_extension.lower().lstrip('.'), instance.target_extension.lower().lstrip('.'))
    _REGISTRY[key] = converter_cls

# Register all converter groups
for converter_cls in (*TEXT_CONVERTERS, *DATA_CONVERTERS, *IMAGE_CONVERTERS):
    register_converter(converter_cls)

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

def list_converters() -> List[Dict[str, Any]]:
    """
    Lists all available conversions, including their option schemas if defined.
    """
    return [
        {
            "source": key[0],
            "target": key[1],
            "options_schema": cls.options_schema.model_json_schema() if cls.options_schema else None
        }
        for key, cls in sorted(_REGISTRY.items())
    ]

def list_source_extensions() -> List[str]:
    """Returns the sorted set of supported source extensions."""
    return sorted({key[0] for key in _REGISTRY})
