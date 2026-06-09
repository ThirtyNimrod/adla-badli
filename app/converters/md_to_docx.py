import pypandoc
from pathlib import Path
from app.converters.base import BaseConverter

class MarkdownToDocxConverter(BaseConverter):
    @property
    def source_extension(self) -> str:
        return "md"

    @property
    def target_extension(self) -> str:
        return "docx"

    def convert(self, input_path: Path, output_path: Path) -> None:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # convert_file will raise RuntimeError if pandoc execution fails
        pypandoc.convert_file(
            source_file=str(input_path),
            to='docx',
            outputfile=str(output_path)
        )
