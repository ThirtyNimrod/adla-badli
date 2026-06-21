import shutil
import uuid
import re
import tempfile
from pathlib import Path
from typing import BinaryIO, Callable, Tuple, Optional
from fastapi import UploadFile

class ConversionWorkspace:
    """
    Manages the lifecycle of temporary files and directories used during conversion.
    Implements a context manager pattern to clean up files unless released.
    """
    def __init__(self, source_ext: str, target_ext: str, base_temp_dir: Optional[Path] = None):
        self.source_ext = source_ext.lower().lstrip('.')
        self.target_ext = target_ext.lower().lstrip('.')
        
        # Security check: whitelist extensions to prevent path traversal
        if not re.match(r'^[a-z0-9]+$', self.source_ext) or not re.match(r'^[a-z0-9]+$', self.target_ext):
            raise ValueError(f"Invalid file extension format: {self.source_ext} or {self.target_ext}")
            
        self.base_temp_dir = base_temp_dir
        self._temp_dir_obj: Optional[tempfile.TemporaryDirectory] = None
        self.workspace_dir: Optional[Path] = None
        self.input_path: Optional[Path] = None
        self.output_path: Optional[Path] = None
        self._released = False

    def __enter__(self) -> "ConversionWorkspace":
        if self.base_temp_dir is not None:
            # Use base temp directory (e.g. for testing)
            self.workspace_dir = Path(self.base_temp_dir) / uuid.uuid4().hex
            self.workspace_dir.mkdir(parents=True, exist_ok=True)
        else:
            # Use safe system temp directory
            self._temp_dir_obj = tempfile.TemporaryDirectory(prefix="adla_")
            self.workspace_dir = Path(self._temp_dir_obj.name)
            
        self.input_path = self.workspace_dir / f"input.{self.source_ext}"
        self.output_path = self.workspace_dir / f"output.{self.target_ext}"
        return self

    def write_input(self, file_stream: BinaryIO) -> Tuple[Path, Path]:
        """
        Writes binary data from a stream to the input path within the workspace.
        Implements a 50 MB file size limit while writing.
        Returns the tuple of (input_path, output_path).
        """
        if self.workspace_dir is None or not self.workspace_dir.exists():
            raise RuntimeError("Workspace directory does not exist. Did you enter the context manager?")
            
        max_upload_bytes = 50 * 1024 * 1024  # 50 MB limit
        total_bytes = 0
        
        with self.input_path.open("wb") as buffer:
            while True:
                chunk = file_stream.read(8192)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > max_upload_bytes:
                    raise ValueError("File exceeds maximum allowed size of 50 MB.")
                buffer.write(chunk)
                
        return self.input_path, self.output_path

    def write_input_file(self, upload_file: UploadFile) -> Tuple[Path, Path]:
        """Helper that accepts a FastAPI UploadFile object and writes its content."""
        return self.write_input(upload_file.file)

    def release(self) -> None:
        """Disarms the automatic cleanup during context exit, delegating it to background tasks."""
        self._released = True

    def get_cleanup_task(self) -> Callable[[], None]:
        """Returns a thread-safe callback that deletes the workspace directory."""
        temp_dir_obj = self._temp_dir_obj
        workspace_dir = self.workspace_dir
        
        def cleanup():
            try:
                if temp_dir_obj is not None:
                    temp_dir_obj.cleanup()
                elif workspace_dir is not None and workspace_dir.exists():
                    shutil.rmtree(workspace_dir)
            except Exception as e:
                # Log cleanup errors using the application logger
                import logging
                logger = logging.getLogger("adla_badli")
                logger.error(f"Error performing background workspace cleanup for {workspace_dir}: {e}", exc_info=True)
                
        return cleanup

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Destroys the workspace directory unless release() has been called."""
        if not self._released:
            cleanup = self.get_cleanup_task()
            cleanup()
