import shutil
import uuid
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
        
        if base_temp_dir is None:
            self.base_temp_dir = Path(__file__).resolve().parent.parent / "temp_uploads"
        else:
            self.base_temp_dir = base_temp_dir
            
        self.workspace_id = uuid.uuid4().hex
        self.workspace_dir = self.base_temp_dir / self.workspace_id
        
        self.input_path = self.workspace_dir / f"input.{self.source_ext}"
        self.output_path = self.workspace_dir / f"output.{self.target_ext}"
        
        self._released = False

    def __enter__(self) -> "ConversionWorkspace":
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        return self

    def write_input(self, file_stream: BinaryIO) -> Tuple[Path, Path]:
        """
        Writes binary data from a stream to the input path within the workspace.
        Returns the tuple of (input_path, output_path).
        """
        if not self.workspace_dir.exists():
            raise RuntimeError("Workspace directory does not exist. Did you enter the context manager?")
            
        with self.input_path.open("wb") as buffer:
            shutil.copyfileobj(file_stream, buffer)
            
        return self.input_path, self.output_path

    def write_input_file(self, upload_file: UploadFile) -> Tuple[Path, Path]:
        """Helper that accepts a FastAPI UploadFile object and writes its content."""
        return self.write_input(upload_file.file)

    def release(self) -> None:
        """Disarms the automatic cleanup during context exit, delegating it to background tasks."""
        self._released = True

    def get_cleanup_task(self) -> Callable[[], None]:
        """Returns a thread-safe callback that deletes the workspace directory."""
        workspace_dir = self.workspace_dir
        
        def cleanup():
            try:
                if workspace_dir.exists():
                    shutil.rmtree(workspace_dir)
            except Exception as e:
                # Log errors in background cleanup silently
                print(f"Error performing background workspace cleanup for {workspace_dir}: {e}")
                
        return cleanup

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Destroys the workspace directory unless release() has been called."""
        if not self._released:
            cleanup = self.get_cleanup_task()
            cleanup()
