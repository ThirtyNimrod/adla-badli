from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Type
from pydantic import BaseModel

class BaseConverter(ABC):
    @property
    @abstractmethod
    def source_extension(self) -> str:
        """The source file extension (e.g., 'md' or 'svg') without leading dot."""
        pass

    @property
    @abstractmethod
    def target_extension(self) -> str:
        """The target file extension (e.g., 'docx' or 'jpg') without leading dot."""
        pass

    # Dynamic options schema defined as a class Pydantic model
    options_schema: Optional[Type[BaseModel]] = None

    @abstractmethod
    def convert(self, input_path: Path, output_path: Path, options: Optional[BaseModel] = None) -> None:
        """Performs the conversion. Raises exceptions on failure."""
        pass
