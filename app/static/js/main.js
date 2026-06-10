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
    const resetBtn = document.getElementById("reset-btn");

    const errorToast = document.getElementById("error-toast");
    const errorToastMsg = document.getElementById("error-toast-message");
    const errorToastClose = document.getElementById("error-toast-close");

    const dynamicOptionsContainer = document.getElementById("dynamic-options-container");

    let selectedFile = null;

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

        try {
            const response = await fetch("/api/convert", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                
                // Create transient object URL
                const url = window.URL.createObjectURL(blob);
                downloadLink.href = url;
                
                // Resolve download filename
                const lastDotIdx = selectedFile.name.lastIndexOf('.');
                const stem = lastDotIdx !== -1 ? selectedFile.name.substring(0, lastDotIdx) : selectedFile.name;
                downloadLink.download = `${stem}.${targetExt}`;
                
                // Transition screens
                loader.classList.add("hidden");
                successOverlay.classList.remove("hidden");
                
                // Trigger programmatic auto-download
                downloadLink.click();
            } else {
                const errJson = await response.json();
                showError(errJson.detail || "An error occurred during file conversion.");
                loader.classList.add("hidden");
            }
        } catch (err) {
            showError("Network error: Could not complete connection to conversion server.");
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
    }

    resetBtn.addEventListener("click", resetState);
    removeFileBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        resetState();
    });

    // Error notifications utilities
    function showError(message) {
        errorToastMsg.textContent = message;
        errorToast.classList.remove("hidden");
    }

    function hideError() {
        errorToast.classList.add("hidden");
    }

    errorToastClose.addEventListener("click", hideError);

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
