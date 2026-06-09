import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.converters import get_converter, list_converters
from app.workspace import ConversionWorkspace

app = FastAPI(title="Adla-Badli File Converter Suite")

# Directories configuration
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure static and templates exist, and mount static path
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

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
    request: Request,
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
    
    # Parse dynamic option parameters from form data
    form_data = await request.form()
    raw_options = {k: v for k, v in form_data.items() if k not in ("file", "target_ext")}
    
    validated_options = None
    if converter.options_schema:
        try:
            validated_options = converter.options_schema.model_validate(raw_options)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

    # Instantiate the workspace to encapsulate file lifetime
    with ConversionWorkspace(source_ext, target_ext) as workspace:
        # Write the upload stream to temporary files inside workspace
        try:
            input_path, output_path = workspace.write_input_file(file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to write uploaded file to disk: {e}")
            
        # Execute conversion
        try:
            converter.convert(input_path, output_path, options=validated_options)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")
            
        # Target download name
        original_stem = Path(original_filename).stem
        download_filename = f"{original_stem}.{target_ext}"
        
        # Defer cleanup to FastAPI background tasks and release workspace context ownership
        background_tasks.add_task(workspace.get_cleanup_task())
        workspace.release()
        
        return FileResponse(
            path=output_path,
            filename=download_filename,
            media_type="application/octet-stream"
        )
