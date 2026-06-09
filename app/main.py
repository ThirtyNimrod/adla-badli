import os
import shutil
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.converters import get_converter, list_converters

app = FastAPI(title="Adla-Badli File Converter Suite")

# Directories configuration
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / "temp_uploads"
TEMP_DIR.mkdir(exist_ok=True)

# Ensure static and templates exist, and mount static path
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

def cleanup_files(*filepaths: Path):
    """Safely cleans up temporary files after sending the HTTP response."""
    for path in filepaths:
        try:
            if path.exists():
                path.unlink()
        except Exception as e:
            # Silently log errors in background cleanup
            print(f"Error performing background cleanup for {path}: {e}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main single page app dashboard."""
    return templates.TemplateResponse(request, "index.html")

@app.get("/api/converters")
async def get_available_converters():
    """Returns a list of supported source-to-target conversions."""
    try:
        return list_converters()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/convert")
async def convert_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    target_ext: str = Form(...),
):
    """
    Accepts a file upload, detects its extension, resolves the correct converter,
    performs conversion, and returns the converted file as an attachment.
    """
    original_filename = file.filename
    if not original_filename:
        raise HTTPException(status_code=400, detail="Invalid upload: missing filename.")
    
    source_ext = Path(original_filename).suffix.lower().lstrip('.')
    target_ext = target_ext.lower().lstrip('.')
    
    if not source_ext:
        raise HTTPException(status_code=400, detail="Uploaded file lacks a valid file extension.")
        
    try:
        converter = get_converter(source_ext, target_ext)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported conversion path from .{source_ext} to .{target_ext}."
        )
    
    # Setup unique temporary paths to prevent file collisions during concurrent requests
    session_id = uuid.uuid4().hex
    input_filename = f"{session_id}_input.{source_ext}"
    output_filename = f"{session_id}_output.{target_ext}"
    
    input_path = TEMP_DIR / input_filename
    output_path = TEMP_DIR / output_filename
    
    # Save upload stream
    try:
        with input_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        cleanup_files(input_path)
        raise HTTPException(status_code=500, detail=f"Failed to write uploaded file to disk: {e}")
        
    # Execute conversion
    try:
        converter.convert(input_path, output_path)
    except Exception as e:
        cleanup_files(input_path, output_path)
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
        
    # Target download name
    original_stem = Path(original_filename).stem
    download_filename = f"{original_stem}.{target_ext}"
    
    # Register background task to clean up files AFTER sending the FileResponse
    background_tasks.add_task(cleanup_files, input_path, output_path)
    
    return FileResponse(
        path=output_path,
        filename=download_filename,
        media_type="application/octet-stream"
    )
