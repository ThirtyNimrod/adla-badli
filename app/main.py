import os
import time
import uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.concurrency import run_in_threadpool
from pydantic import ValidationError

from app.converters import get_converter, list_converters
from app.workspace import ConversionWorkspace
from app.logger import logger, request_id_var

app = FastAPI(title="Adla-Badli File Converter Suite")

# Directories configuration
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure static and templates exist, and mount static path
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

# MIME Type Allowlist per source extension
ALLOWED_MIMES = {
    "md": {"text/markdown", "text/x-markdown", "text/plain", "application/octet-stream", ""},
    "txt": {"text/plain", "application/octet-stream", ""},
    "html": {"text/html", "application/octet-stream", ""},
    "csv": {"text/csv", "text/plain", "application/csv", "text/x-csv", "application/octet-stream", ""},
    "json": {"application/json", "text/json", "text/plain", "application/octet-stream", ""},
    "svg": {"image/svg+xml", "text/xml", "application/xml", "application/octet-stream", ""},
    "xlsx": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/octet-stream", ""},
    "docx": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/octet-stream", ""},
    "pdf": {"application/pdf", "application/octet-stream", ""},
}

# Middleware for request ID and JSON structured logging
@app.middleware("http")
async def add_request_id_and_logging(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    request_id_var.set(req_id)
    
    start_time = time.time()
    logger.info(f"Started request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        response.headers["X-Request-ID"] = req_id
        logger.info(
            f"Finished request: {request.method} {request.url.path} with status {response.status_code}",
            extra={"duration": duration}
        )
        return response
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path} - {str(e)}",
            exc_info=True,
            extra={"duration": duration}
        )
        raise

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serves the favicon icon to prevent 404 log clutter."""
    return FileResponse(BASE_DIR / "app" / "static" / "favicon.png")

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
        logger.error(f"Failed to list converters: {e}", exc_info=True)
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
        logger.warning("Upload rejected: missing filename.")
        raise HTTPException(status_code=400, detail="Invalid upload: missing filename.")
    
    source_ext = Path(original_filename).suffix.lower().lstrip('.')
    target_ext = target_ext.lower().lstrip('.')
    
    if not source_ext:
        logger.warning(f"Upload rejected: no extension in filename '{original_filename}'.")
        raise HTTPException(status_code=400, detail="Uploaded file lacks a valid file extension.")
        
    # Content-Length check (limit 50 MB)
    content_length = request.headers.get("content-length")
    max_upload_bytes = 50 * 1024 * 1024
    if content_length:
        try:
            if int(content_length) > max_upload_bytes:
                logger.warning(f"Upload rejected: file size header {content_length} exceeds limit of 50 MB.")
                raise HTTPException(
                    status_code=413,
                    detail="File exceeds maximum allowed size of 50 MB."
                )
        except ValueError:
            pass

    # MIME Type Validation
    content_type = file.content_type
    if content_type is not None:
        allowed_mimes = ALLOWED_MIMES.get(source_ext)
        if allowed_mimes and content_type not in allowed_mimes:
            logger.warning(f"Upload rejected: MIME type '{content_type}' is invalid for .{source_ext} files.")
            raise HTTPException(
                status_code=400,
                detail=f"MIME type '{content_type}' is invalid for .{source_ext} files."
            )

    try:
        converter = get_converter(source_ext, target_ext)
    except ValueError as e:
        logger.warning(f"Upload rejected: unsupported conversion path from .{source_ext} to .{target_ext}.")
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported conversion path from .{source_ext} to .{target_ext}."
        )
    
    logger.info(f"Converter selected: {converter.__class__.__name__} for .{source_ext} to .{target_ext}")

    # Parse dynamic option parameters from form data
    form_data = await request.form()
    raw_options = {k: v for k, v in form_data.items() if k not in ("file", "target_ext")}
    
    validated_options = None
    if converter.options_schema:
        try:
            validated_options = converter.options_schema.model_validate(raw_options)
            logger.info("Successfully validated converter options.")
        except ValidationError as e:
            logger.warning(f"Options validation failed: {e.errors()}")
            raise HTTPException(status_code=422, detail=e.errors())

    # Instantiate the workspace to encapsulate file lifetime
    try:
        workspace_ctx = ConversionWorkspace(source_ext, target_ext)
    except ValueError as e:
        logger.warning(f"Workspace creation rejected: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    with workspace_ctx as workspace:
        # Write the upload stream to temporary files inside workspace
        try:
            input_path, output_path = workspace.write_input_file(file)
        except ValueError as e:
            # File size limit raised during writing
            logger.warning(f"Write aborted: {e}")
            raise HTTPException(status_code=413, detail=str(e))
        except Exception as e:
            logger.error(f"Failed to write uploaded file to disk: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to write uploaded file to disk: {str(e)}")
            
        # Execute conversion asynchronously in the threadpool
        start_time = time.time()
        try:
            await run_in_threadpool(converter.convert, input_path, output_path, options=validated_options)
            duration = time.time() - start_time
            logger.info(f"Successfully converted file in {duration:.4f} seconds.")
        except ValueError as e:
            logger.warning(f"Conversion input parsing error: {e}")
            raise HTTPException(status_code=422, detail=f"File could not be parsed: {str(e)}")
        except OSError as e:
            # Check for Pandoc missing
            err_msg = str(e)
            if "pandoc" in err_msg.lower():
                logger.error(f"System dependency error: Pandoc is missing on the server - {e}", exc_info=True)
                raise HTTPException(status_code=503, detail="A required system dependency (Pandoc) is missing on the server.")
            # Check for disk full
            elif e.errno == 28: # ENOSPC
                logger.error(f"System resource error: Disk is full - {e}", exc_info=True)
                raise HTTPException(status_code=507, detail="Server disk space is exhausted.")
            else:
                logger.error(f"IO error during conversion: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Conversion system error: {err_msg}")
        except Exception as e:
            logger.error(f"Unexpected conversion error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Conversion failed due to an internal error: {str(e)}")
            
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
