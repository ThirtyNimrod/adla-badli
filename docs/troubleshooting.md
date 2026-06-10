# Troubleshooting Guide

This guide details resolutions for common issues encountered while setting up, running, or developing the **Adla-Badli File Converter Suite**.

---

## 1. Port 8000 Already in Use (Address already in use / Access Forbidden)

### Problem
When starting the Uvicorn server with `uvicorn app.main:app --reload`, you receive an error like:
```plaintext
ERROR:    [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions
```
or
```plaintext
ERROR:    [Errno 98] Address already in use
```

This happens when another process (like a previously orphaned Uvicorn instance or another service) is already listening on port `8000`.

### Solution (Windows)
To free up port `8000`, locate the process hoarding it and terminate it:

1. Open **PowerShell** or **Command Prompt** (as Administrator if required) and run the following command to find the Process ID (PID):
   ```cmd
   netstat -ano | findstr :8000
   ```
   *Note: In PowerShell, you can also use `Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess`.*

2. You will see output resembling this (the last column is the PID):
   ```plaintext
     TCP    127.0.0.1:8000         0.0.0.0:0              LISTENING       3156
   ```

3. Forcefully kill the process using its PID (replace `3156` with the actual PID from your output):
   ```cmd
   taskkill /PID 3156 /F
   ```

4. Restart your application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Solution (macOS / Linux)
1. Find the PID using the port:
   ```bash
   lsof -i :8000
   ```
2. Terminate the process (replace `<PID>` with the actual Process ID shown in the command output):
   ```bash
   kill -9 <PID>
   ```

---

## 2. Pandoc Errors (Markdown / Document Conversions)

### Problem
Conversions involving `md`, `txt`, or `html` to document formats fail, and you see errors like:
```plaintext
OSError: No pandoc was found on your system. Please install pandoc...
```
or converter unit tests fail on text-based tests.

### Solution
Pandoc must be installed on your system. You can install it globally or download a project-local binary via `pypandoc`:

* **Automatic / Project-Local (Python-based):**
  Run the following command inside your activated virtual environment:
  ```bash
  python -m pypandoc.download_pandoc
  ```
  This downloads and configures the Pandoc binary locally for Python.

* **System-wide Installation:**
  * **Windows (via Winget / Chocolatey):**
    ```powershell
    winget install JohnMacFarlane.Pandoc
    # or
    choco install pandoc
    ```
  * **macOS (via Homebrew):**
    ```bash
    brew install pandoc
    ```
  * **Linux (Ubuntu/Debian):**
    ```bash
    sudo apt update && sudo apt install pandoc
    ```
  *After system-wide installation, make sure to restart your terminal/IDE for the PATH changes to take effect.*

---

## 3. Playwright E2E Test Failures

### Problem
Running `npm run test:e2e` fails with messages indicating that browsers are missing:
```plaintext
Error: browserType.launch: Executable doesn't exist at C:\Users\...
```
Or tests time out because the local server cannot start.

### Solution
1. Ensure all Node.js dependencies are installed:
   ```bash
   npm install
   ```
2. Install the required Playwright browser binaries:
   ```bash
   npx playwright install
   ```
3. If the tests fail because of port conflicts, make sure port `8000` is free before running the tests (see [Section 1](#1-port-8000-already-in-use-address-already-in-use--access-forbidden)). Playwright starts its own instance of the Uvicorn server on port `8000` via its `webServer` config. If you already have Uvicorn running in another terminal, you should stop it before running `npm run test:e2e`.

---

## 4. xhtml2pdf & ReportLab Layout/Font Issues

### Problem
Converted PDFs have garbled text, boxes (`[]`) instead of characters, or formatting is severely broken.

### Solution
* **Special Characters / Fonts:** `xhtml2pdf` and `ReportLab` rely on standard Helvetica/Times-Roman fonts by default, which may not support all Unicode ranges (like emoji or non-Latin glyphs). If your documents contain special characters, check the SVGs or source HTML. SVG text should ideally be converted to paths, or use standard fonts.
* **Complex CSS Layouts:** `xhtml2pdf` only supports a subset of HTML/CSS. If converting HTML with modern features (like CSS Grid or Flexbox), the rendering will fail or degrade. Simplify the input HTML to standard tables, blocks, and basic inline formatting.

---

## 5. Temporary Upload / Workspace Permissions

### Problem
You get `PermissionError` when uploading files or running tests, or the backend fails to clean up directories.

### Solution
* **Write Permissions:** Make sure the application has write access to the workspace directory. By default, Adla-Badli creates directories inside Windows' temporary directory (`%TEMP%`) and a local `temp_uploads` folder if needed.
* **File Locks (Windows):** Windows prevents deleting files that are still open by a process. If a converter does not properly close file handles to the source or output file, the background cleanup task will fail to delete the temporary workspace. Ensure all converters wrap file handles in context managers (`with open(...)`).
