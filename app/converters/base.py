from abc import ABC, abstractmethod
from pathlib import Path

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

    @abstractmethod
    def convert(self, input_path: Path, output_path: Path, **kwargs) -> None:
        """Performs the conversion. Raises exceptions on failure."""
        pass
