document.addEventListener("DOMContentLoaded", () => {
    // API endpoint mappings
    let supportedConversions = [];

    // Cache DOM Elements
    const dropzone = document.getElementById("file-dropzone");
    const fileInput = document.getElementById("file-input");
    const dropzonePrompt = document.getElementById("dropzone-prompt");
    const fileDetails = document.getElementById("file-details");
    const fileBadge = document.getElementById("file-badge-ext");
    const fileName = document.getElementById("selected-file-name");
    const fileSize = document.getElementById("selected-file-size");
    const removeFileBtn = document.getElementById("remove-file-btn");

    const controls = document.getElementById("converter-controls");
    const targetSelect = document.getElementById("target-select");
    const convertBtn = document.getElementById("convert-btn");

    const loader = document.getElementById("loader-overlay");
    const successOverlay = document.getElementById("success-overlay");
    const downloadLink = document.getElementById("download-link");
    const previewBtn = document.getElementById("preview-btn");
    const resetBtn = document.getElementById("reset-btn");

    const errorToast = document.getElementById("error-toast");
    const errorToastMsg = document.getElementById("error-toast-message");
    const errorToastClose = document.getElementById("error-toast-close");

    const dynamicOptionsContainer = document.getElementById("dynamic-options-container");
    const previewContainer = document.getElementById("preview-container");
    const previewContent = document.getElementById("preview-content");
    const previewCloseBtn = document.getElementById("preview-close-btn");

    const inputPreviewContainer = document.getElementById("input-preview-container");
    const inputPreviewToggle = document.getElementById("input-preview-toggle");
    const inputPreviewContent = document.getElementById("input-preview-content");

    let selectedFile = null;
    let convertedBlob = null;
    let convertedTargetExt = "";
    let convertedUrl = "";

    // 1. Fetch available converters dynamically from backend
    async function loadConverters() {
        try {
            const response = await fetch("/api/converters");
            if (response.ok) {
                supportedConversions = await response.json();
            } else {
                showError("Could not retrieve supported file types from backend server.");
            }
        } catch (e) {
            showError("Network error: Could not reach backend converter API.");
        }
    }
    loadConverters();

    // 2. Drag & Drop Event Listeners
    ["dragenter", "dragover"].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.add("dragover");
        }, false);
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropzone.classList.remove("dragover");
        }, false);
    });

    dropzone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // Click on dropzone triggers file dialog, unless clicking interactive child items
    dropzone.addEventListener("click", (e) => {
        if (e.target.closest("#remove-file-btn") || e.target.closest("#file-details")) {
            return;
        }
        fileInput.click();
    });

    // Keyboard navigation: Enter/Space triggers upload
    dropzone.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            if (e.target.closest("#remove-file-btn") || e.target.closest("#file-details")) {
                return;
            }
            e.preventDefault();
            fileInput.click();
        }
    });

    fileInput.addEventListener("change", (e) => {
        if (fileInput.files.length > 0) {
            handleFileSelect(fileInput.files[0]);
        }
    });

    // 3. File Selection Action
    function handleFileSelect(file) {
        if (file.size > 50 * 1024 * 1024) {
            showError("File is too large. Maximum size allowed is 50 MB.");
            resetState();
            return;
        }
        selectedFile = file;
        
        // Show file details card
        const ext = file.name.split('.').pop().toLowerCase();
        fileBadge.textContent = ext.toUpperCase();
        fileName.textContent = file.name;
        fileSize.textContent = formatBytes(file.size);

        dropzonePrompt.classList.add("hidden");
        fileDetails.classList.remove("hidden");

        // Filter and show targets options
        populateTargets(ext);

        // Reset and generate preview
        if (inputPreviewContainer) inputPreviewContainer.classList.add("hidden");
        if (inputPreviewContent) {
            inputPreviewContent.classList.add("hidden");
            inputPreviewContent.innerHTML = "";
        }
        if (inputPreviewToggle) {
            const toggleSpan = inputPreviewToggle.querySelector("span");
            if (toggleSpan) toggleSpan.textContent = "Show File Preview";
            const chevron = inputPreviewToggle.querySelector(".chevron-icon");
            if (chevron) chevron.style.transform = "rotate(0deg)";
        }
        generateInputPreview(file, ext);
    }

    // 4. Update Target Output Formats select options
    function populateTargets(sourceExt) {
        // Clear previous options
        targetSelect.innerHTML = '<option value="" disabled selected>Select output format…</option>';
        
        // Match possible output targets for the selected file type
        const targets = supportedConversions
            .filter(conv => conv.source.toLowerCase() === sourceExt.toLowerCase())
            .map(conv => conv.target);

        if (targets.length === 0) {
            const supported = [...new Set(supportedConversions.map(conv => conv.source))].sort().join(", .");
            showError(`Unsupported file type: .${sourceExt}. Supported source formats: .${supported}`);
            resetState();
            return;
        }

        targets.forEach(target => {
            const opt = document.createElement("option");
            opt.value = target;
            opt.textContent = target.toUpperCase();
            targetSelect.appendChild(opt);
        });

        // Show configuration controls
        controls.classList.remove("hidden");

        // Auto-select option if there's only one output candidate
        if (targets.length === 1) {
            targetSelect.value = targets[0];
            renderDynamicOptions(sourceExt, targets[0]);
        } else {
            dynamicOptionsContainer.innerHTML = "";
        }
    }

    targetSelect.addEventListener("change", () => {
        if (selectedFile) {
            const ext = selectedFile.name.split('.').pop().toLowerCase();
            renderDynamicOptions(ext, targetSelect.value);
        }
    });

    function renderDynamicOptions(sourceExt, targetExt) {
        dynamicOptionsContainer.innerHTML = "";
        
        const converter = supportedConversions.find(
            conv => conv.source.toLowerCase() === sourceExt.toLowerCase() && 
                    conv.target.toLowerCase() === targetExt.toLowerCase()
        );
        
        if (!converter || !converter.options_schema || !converter.options_schema.properties) {
            return;
        }
        
        const properties = converter.options_schema.properties;
        
        for (const [name, prop] of Object.entries(properties)) {
            const controlGroup = document.createElement("div");
            controlGroup.className = "control-group";
            
            const label = document.createElement("label");
            label.className = "control-label";
            label.setAttribute("for", `option-${name}`);
            label.textContent = prop.title || name;
            controlGroup.appendChild(label);
            
            if (prop.enum) {
                const selectWrapper = document.createElement("div");
                selectWrapper.className = "select-wrapper";
                
                const select = document.createElement("select");
                select.id = `option-${name}`;
                select.name = name;
                select.className = "target-select";
                
                prop.enum.forEach(val => {
                    const opt = document.createElement("option");
                    opt.value = val;
                    opt.textContent = val.charAt(0).toUpperCase() + val.slice(1);
                    if (val === prop.default) {
                        opt.selected = true;
                    }
                    select.appendChild(opt);
                });
                
                selectWrapper.appendChild(select);
                controlGroup.appendChild(selectWrapper);
            } else if (prop.type === "boolean") {
                const checkbox = document.createElement("input");
                checkbox.id = `option-${name}`;
                checkbox.type = "checkbox";
                checkbox.name = name;
                checkbox.className = "option-checkbox";
                checkbox.checked = prop.default || false;
                controlGroup.appendChild(checkbox);
            } else {
                const input = document.createElement("input");
                input.id = `option-${name}`;
                input.name = name;
                input.className = "option-input";
                input.type = prop.type === "integer" || prop.type === "number" ? "number" : "text";
                input.value = prop.default !== undefined ? prop.default : "";
                controlGroup.appendChild(input);
            }
            
            dynamicOptionsContainer.appendChild(controlGroup);
        }
    }

    // 5. Submit conversion request to API
    convertBtn.addEventListener("click", async () => {
        if (!selectedFile) {
            showError("Please upload a file first.");
            return;
        }
        const targetExt = targetSelect.value;
        if (!targetExt) {
            showError("Please choose a target conversion format.");
            return;
        }

        // Show progress overlay
        loader.classList.remove("hidden");
        hideError();

        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("target_ext", targetExt);
        
        // Dynamically capture parameters from dynamic options container
        const inputs = dynamicOptionsContainer.querySelectorAll("input, select");
        inputs.forEach(input => {
            if (input.type === "checkbox") {
                formData.append(input.name, input.checked ? "true" : "false");
            } else {
                formData.append(input.name, input.value);
            }
        });

        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
            controller.abort();
        }, 120000); // 2 minutes

        const loaderDetails = document.getElementById("loader-details");
        if (loaderDetails) {
            loaderDetails.textContent = "Applying styles and rendering structure.";
        }

        const warningTimeoutId = setTimeout(() => {
            if (loaderDetails) {
                loaderDetails.textContent = "Taking longer than expected… please wait.";
            }
        }, 30000); // 30 seconds

        try {
            const response = await fetch("/api/convert", {
                method: "POST",
                body: formData,
                signal: controller.signal
            });

            if (response.ok) {
                clearTimeout(timeoutId);
                clearTimeout(warningTimeoutId);
                const blob = await response.blob();
                
                // Store converted info for previewing
                convertedBlob = blob;
                convertedTargetExt = targetExt;
                
                // Create transient object URL
                const url = window.URL.createObjectURL(blob);
                convertedUrl = url;
                downloadLink.href = url;
                
                // Resolve download filename
                const lastDotIdx = selectedFile.name.lastIndexOf('.');
                const stem = lastDotIdx !== -1 ? selectedFile.name.substring(0, lastDotIdx) : selectedFile.name;
                downloadLink.download = `${stem}.${targetExt}`;
                
                // Transition screens
                loader.classList.add("hidden");
                successOverlay.classList.remove("hidden");
            } else {
                clearTimeout(timeoutId);
                clearTimeout(warningTimeoutId);
                let detailMsg = "";
                try {
                    const errJson = await response.json();
                    detailMsg = errJson.detail;
                    if (typeof detailMsg !== "string" && Array.isArray(detailMsg)) {
                        detailMsg = detailMsg.map(err => `${err.loc.join('.')}: ${err.msg}`).join(', ');
                    }
                } catch (e) {}

                let errMsg = "";
                if (response.status === 413) {
                    errMsg = detailMsg || "File is too large. Please upload a file under 50 MB.";
                } else if (response.status === 422) {
                    errMsg = detailMsg || "File could not be read. Check that it is a valid file.";
                } else if (response.status === 503) {
                    errMsg = detailMsg || "A required system tool is missing on the server.";
                } else {
                    errMsg = detailMsg || `Conversion failed (Status Code ${response.status}).`;
                }
                showError(errMsg);
                loader.classList.add("hidden");
            }
        } catch (err) {
            clearTimeout(timeoutId);
            clearTimeout(warningTimeoutId);
            if (err.name === 'AbortError') {
                showError("Conversion timed out. The server took longer than 2 minutes to respond.");
            } else {
                showError("Network error: Could not complete connection to conversion server.");
            }
            loader.classList.add("hidden");
        }
    });

    // 6. Reset views for a new run
    function resetState() {
        selectedFile = null;
        fileInput.value = "";
        dropzonePrompt.classList.remove("hidden");
        fileDetails.classList.add("hidden");
        controls.classList.add("hidden");
        successOverlay.classList.add("hidden");
        dynamicOptionsContainer.innerHTML = "";
        targetSelect.innerHTML = '<option value="" disabled selected>Select output format…</option>';
        hideError();

        // Reset input preview state
        if (inputPreviewContainer) inputPreviewContainer.classList.add("hidden");
        if (inputPreviewContent) {
            inputPreviewContent.classList.add("hidden");
            inputPreviewContent.innerHTML = "";
        }
        if (inputPreviewToggle) {
            const toggleSpan = inputPreviewToggle.querySelector("span");
            if (toggleSpan) toggleSpan.textContent = "Show File Preview";
            const chevron = inputPreviewToggle.querySelector(".chevron-icon");
            if (chevron) chevron.style.transform = "rotate(0deg)";
        }

        // Revoke preview URL and clean up states
        if (convertedUrl) {
            window.URL.revokeObjectURL(convertedUrl);
            convertedUrl = "";
        }
        convertedBlob = null;
        convertedTargetExt = "";
        previewContainer.classList.add("hidden");
        previewContent.innerHTML = "";
    }

    resetBtn.addEventListener("click", resetState);
    removeFileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        resetState();
    });
    previewBtn.addEventListener("click", showPreview);
    previewCloseBtn.addEventListener("click", closePreview);

    if (inputPreviewToggle) {
        inputPreviewToggle.addEventListener("click", (e) => {
            e.stopPropagation(); // prevent triggering dropzone click
            if (inputPreviewContent) {
                const isHidden = inputPreviewContent.classList.toggle("hidden");
                const toggleSpan = inputPreviewToggle.querySelector("span");
                const chevron = inputPreviewToggle.querySelector(".chevron-icon");
                if (toggleSpan) toggleSpan.textContent = isHidden ? "Show File Preview" : "Hide File Preview";
                if (chevron) chevron.style.transform = isHidden ? "rotate(0deg)" : "rotate(180deg)";
            }
        });
    }

    function closePreview() {
        previewContainer.classList.add("hidden");
        previewContent.innerHTML = "";
    }

    async function showPreview() {
        if (!convertedBlob || !convertedTargetExt) {
            showError("No converted file available to preview.");
            return;
        }

        // Clean previous preview contents
        previewContent.innerHTML = "";
        previewContainer.classList.remove("hidden");
        
        // Ensure preview container is visible and scroll into it smoothly
        previewContainer.scrollIntoView({ behavior: "smooth", block: "nearest" });

        const ext = convertedTargetExt.toLowerCase();

        // 1. Image formats (PNG, JPG, SVG)
        if (["png", "jpg", "jpeg", "svg"].includes(ext)) {
            const img = document.createElement("img");
            img.src = convertedUrl;
            img.className = "preview-image";
            img.alt = "File Preview";
            
            const wrapper = document.createElement("div");
            wrapper.className = "preview-image-wrapper";
            wrapper.appendChild(img);
            previewContent.appendChild(wrapper);
        }
        // 2. PDF
        else if (ext === "pdf") {
            const iframe = document.createElement("iframe");
            iframe.src = `${convertedUrl}#toolbar=0`;
            iframe.className = "preview-iframe";
            previewContent.appendChild(iframe);
        }
        // 3. HTML
        else if (ext === "html") {
            const iframe = document.createElement("iframe");
            iframe.className = "preview-iframe";
            iframe.sandbox = "allow-same-origin";
            previewContent.appendChild(iframe);
            try {
                const text = await convertedBlob.text();
                iframe.srcdoc = text;
            } catch (e) {
                previewContent.textContent = "Error loading HTML preview: " + e.message;
            }
        }
        // 4. Text and JSON
        else if (["txt", "json"].includes(ext)) {
            try {
                let text = await convertedBlob.text();
                if (ext === "json") {
                    try {
                        const jsonObj = JSON.parse(text);
                        text = JSON.stringify(jsonObj, null, 2);
                    } catch (err) {
                        // Keep text as-is if parsing fails
                    }
                }
                const pre = document.createElement("pre");
                pre.className = "preview-text-block";
                const code = document.createElement("code");
                code.textContent = text;
                pre.appendChild(code);
                previewContent.appendChild(pre);
            } catch (e) {
                previewContent.textContent = "Error loading text preview: " + e.message;
            }
        }
        // 5. CSV
        else if (ext === "csv") {
            try {
                const text = await convertedBlob.text();
                previewContent.innerHTML = renderCsvPreview(text);
            } catch (e) {
                previewContent.textContent = "Error loading CSV preview: " + e.message;
            }
        }
        // 6. Word / Excel fallback placeholders
        else if (["docx", "xlsx"].includes(ext)) {
            const isExcel = ext === "xlsx";
            const iconSvg = isExcel ? 
                `<svg class="preview-placeholder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                    <line x1="3" y1="9" x2="21" y2="9" />
                    <line x1="9" y1="21" x2="9" y2="9" />
                 </svg>` :
                `<svg class="preview-placeholder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="16" y1="13" x2="8" y2="13" />
                    <line x1="16" y1="17" x2="8" y2="17" />
                    <polyline points="10 9 9 9 8 9" />
                 </svg>`;
            
            const placeholder = document.createElement("div");
            placeholder.className = "preview-placeholder";
            placeholder.innerHTML = `
                ${iconSvg}
                <h4>${isExcel ? "Spreadsheet" : "Document"} Preview Unavailable</h4>
                <p>The <strong>.${ext.toUpperCase()}</strong> format cannot be displayed natively in the web browser. Please click the <strong>Download Output</strong> button to open it locally.</p>
            `;
            previewContent.appendChild(placeholder);
        }
        // Fallback for any other format
        else {
            previewContent.textContent = "Preview not supported for ." + ext + " files. Please download to view.";
        }
    }

    // Escape HTML util
    function escapeHtml(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // CSV line parsing helper that supports quotes/escapes
    function parseCsvLine(text) {
        let p = '', c = '', r = [];
        let q = false;
        for (let i = 0; i < text.length; i++) {
            c = text.charAt(i);
            if (c === '"') {
                q = !q;
            } else if (c === ',' && !q) {
                r.push(p);
                p = '';
            } else {
                p += c;
            }
        }
        r.push(p);
        return r.map(cell => {
            let s = cell.trim();
            if (s.startsWith('"') && s.endsWith('"')) {
                s = s.substring(1, s.length - 1);
            }
            return s;
        });
    }

    // CSV to HTML table renderer
    function renderCsvPreview(text) {
        const lines = text.split(/\r?\n/);
        const rows = lines
            .map(line => parseCsvLine(line))
            .filter(r => r.length > 0 && r.some(cell => cell !== ""));
            
        if (rows.length === 0) {
            return "<p>Empty CSV file</p>";
        }
        
        let html = '<div class="preview-table-wrapper"><table class="preview-table">';
        
        // Header
        html += '<thead><tr>';
        rows[0].forEach(cell => {
            html += `<th>${escapeHtml(cell)}</th>`;
        });
        html += '</tr></thead><tbody>';
        
        // Rows (limit to first 10 for preview performance)
        const maxPreviewRows = 10;
        const dataRows = rows.slice(1, maxPreviewRows + 1);
        
        dataRows.forEach(row => {
            html += '<tr>';
            // Pad or truncate row elements to match header count
            const colsCount = rows[0].length;
            for (let i = 0; i < colsCount; i++) {
                const val = row[i] !== undefined ? row[i] : "";
                html += `<td>${escapeHtml(val)}</td>`;
            }
            html += '</tr>';
        });
        
        html += '</tbody></table></div>';
        
        if (rows.length > maxPreviewRows + 1) {
            html += `<p class="preview-more-rows">Showing first ${maxPreviewRows} of ${rows.length - 1} data rows.</p>`;
        }
        
        return html;
    }

    // Error notifications utilities
    function showError(message) {
        errorToastMsg.textContent = message;
        errorToast.classList.remove("hidden");
    }

    function hideError() {
        errorToast.classList.add("hidden");
    }

    errorToastClose.addEventListener("click", hideError);

    // Escape key listener for error toast dismissal
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            hideError();
        }
    });

    // Generate collapsible preview for selected input file
    function generateInputPreview(file, ext) {
        const textFormats = ["md", "txt", "html", "csv", "json"];
        if (textFormats.includes(ext)) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const text = e.target.result;
                const snippet = text.slice(0, 500) + (text.length > 500 ? "\n... [truncated]" : "");
                
                const pre = document.createElement("pre");
                pre.className = "preview-text-block";
                const code = document.createElement("code");
                code.textContent = snippet;
                pre.appendChild(code);
                
                if (inputPreviewContent) {
                    inputPreviewContent.appendChild(pre);
                    if (inputPreviewContainer) inputPreviewContainer.classList.remove("hidden");
                }
            };
            reader.readAsText(file);
        } else if (ext === "svg") {
            const reader = new FileReader();
            reader.onload = function(e) {
                const dataUrl = e.target.result;
                const img = document.createElement("img");
                img.src = dataUrl;
                img.className = "preview-image";
                img.style.maxHeight = "200px";
                
                const wrapper = document.createElement("div");
                wrapper.className = "preview-image-wrapper";
                wrapper.appendChild(img);
                
                if (inputPreviewContent) {
                    inputPreviewContent.appendChild(wrapper);
                    if (inputPreviewContainer) inputPreviewContainer.classList.remove("hidden");
                }
            };
            reader.readAsDataURL(file);
        }
    }

    // Bytes formatter util
    function formatBytes(bytes, decimals = 1) {
        if (bytes === 0) return "0 Bytes";
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ["Bytes", "KB", "MB", "GB"];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
    }
});
