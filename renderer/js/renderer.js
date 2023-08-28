/**
 * This script handles the user interface interactions and communication with the main process in the Electron renderer process.
 * It initializes various elements, handles events such as file selection, drag-and-drop, form submission, and displays output.
 * 
 * @namespace renderer
 */


// Check that renderer.js app works
console.log("renderer.js is working");


// ELEMENTS INITIALIZATION
const dragDropBox = document.querySelector("#dragDropBox");             // Input elements
const dragDropBoxText = document.querySelector("#dragDropBoxText");
const inFile = document.querySelector("#inFile")
const inFolder = document.querySelector("#inFolder")
const tooltip = document.querySelector("#tooltip")
const outPathButton = document.querySelector("#outPathButton");         // Output elements
const operationSelection = document.querySelector("#operationType");    // Operation elements    
const submitButton = document.querySelector('#submitButton');           // Submit elements
const form = document.getElementById('fileProcessingForm');             // FORM elements
const opArray = ['merge', 'split', 'conform', 'convert'];               // Constants

// VARIABLES
let inPath = undefined;
let outPath = undefined;
let operationType = undefined;



// EVENTS

// OUTPUT PATH HANDLER
outPathButton.addEventListener('click', async () => {
    // Invoke main.js to get path
    const result = await ipcRenderer.invoke('get-path', 'openDirectory');
    // If user actually chooses a dir
    if (!result.canceled) {
        // Update the global variable that will be used in the form
        const selectedPath = result.path;
        outPath = selectedPath
        // Update the value of outPathButton (front-end)
        let printName = getPrintName(outPath);
        outPathButton.textContent = printName;
        // Log user's output folder choice
        console.log("Output Path: ", outPath)
    }
    else {
        if (outPath === undefined) {
            outPathButton.textContent = 'Select a folder';
            alertMessage("Please Select Valid Output Folder", "red");
        };
    }
});

// Operation Type handler EVENT
operationSelection.addEventListener('change', ()=> {
    operationType = operationSelection.value;
    console.log("Operation: ", operationType);
    submitButton.textContent = operationType.toUpperCase();
});



// INPUT PATH HANDLER EVENTS

// Input: Handle mouseover
dragDropBox.addEventListener('mouseover', () => {
    inFile.style.display = 'block';
    inFolder.style.display = 'block';
    dragDropBoxText.style.display = 'none';
});
dragDropBox.addEventListener('mouseout', () => {
    inFile.style.display = 'none';
    inFolder.style.display = 'none';
    dragDropBoxText.style.display = 'block';
});
inFile.addEventListener("mouseover", () => {
    inFile.style.cursor = "pointer";
    inFile.style.filter = "brightness(110%)";
});
inFile.addEventListener("mouseout", () => {
    inFile.style.cursor = "auto";
    inFile.style.filter = "";
});
inFolder.addEventListener("mouseover", () => {
    inFolder.style.cursor = "pointer";
    inFolder.style.filter = "brightness(110%)";
});
inFolder.addEventListener("mouseout", () => {
    inFolder.style.cursor = "auto";
    inFolder.style.filter = "";
});

// Input: Handle clicking
inFile.addEventListener('click', () => {
    handleInPathSelection('openFile')(); // See helper function below
});
inFolder.addEventListener('click', () => {
    handleInPathSelection('openDirectory')();
});

// Input: Handle Drag n Drop functionality
dragDropBox.addEventListener('dragover', (event) => {
    event.preventDefault();
    tooltip.style.display = "block";
    tooltip.style.top = `${event.clientY + 15}px`;
    tooltip.style.left = `${event.clientX + 15}px`; 
    dragDropBox.style.filter = "brightness(110%)";

    // Set what will happen if user actually drops files ('copy')
    event.dataTransfer.dropEffect = 'copy';
  });
dragDropBox.addEventListener("dragleave", (event) => {
    event.preventDefault();
    tooltip.style.display = "none";
    dragDropBox.style.backgroundColor = "";
    dragDropBox.style.filter = "";
});
// Event listener for drag and drop
dragDropBox.addEventListener("drop", async (event) => {
    event.preventDefault();
    tooltip.style.display = "none";
    dragDropBox.style.backgroundColor = "";
    dragDropBox.style.filter = "";

    // Handle dropped files
    const files = Array.from(event.dataTransfer.files);
    const filePaths = files.map((file) => file.path);
    // Send file paths to the main process
    absoluteFilePaths = await ipcRenderer.invoke('files-dropped', filePaths);
    
    if (absoluteFilePaths.length > 1) {
        // Code to execute if the array's length is greater than 1
        console.log('Array has more than 1 elements.');
        // Other actions or logic
        alertMessage("Cannot accept multiple folder or file paths")
    } else {
        // Handle the dropped files here 
        inPath = absoluteFilePaths[0]
    
        console.log(inPath)
    
        if (outPath === undefined || outPathButton.textContent === "Same as input. Click to change.") {
            // Use the abstracted function here
            assingInToOutPath(inPath);
        }
        
        console.log("Input path: ", inPath);
        let printName = getPrintName(`${inPath}`);
        dragDropBoxText.textContent = printName;
    }
});



// FORM/SUBMIT HANDLER EVENT

form.addEventListener("submit", function(event) {
    // MODAL
    const messageModal = new bootstrap.Modal(document.getElementById('messageModal'));

    event.preventDefault(); // Prevent form submission
    
    if (!validateForm()) {
      return alertMessage("Form is not fully filled", "red");
    }

    // Get data
    const inputPath = inPath;
    const outputPath = outPath;
    const operation = operationType;

    // Clear previous output
    document.getElementById('outputText').textContent = '';

    // Send data to main process
    ipcRenderer.send('start-operation', { inputPath, outputPath, operation });


    // Operation Started
    ipcRenderer.on('operation-started', (event, signal) => {
        inFile.style.display = 'none';
        inFolder.style.display = 'none';
        dragDropBoxText.style.display = 'block';
        dragDropBoxText.textContent = "WAIT FOR OPERATION TO FINISH..."
        disableElements();

        
        messageModal.show();
    });
    // Operation Finished
    ipcRenderer.on('operation-finished', (success) => {
        console.log("SUCCESS: ", success)
        if (success === "true") {
            enableElements();
        }
        else {
            alertMessage("Operation FAILED!", "red")
            enableElements();
        }
        dragDropBoxText.textContent = "Drag and drop file or folder here"

        messageModal.hide();
    });



    alertMessage("Operation Started.", "green");
});

// IPC event handler for receiving Python output
ipcRenderer.on('python-output', (event, data) => {
    // Append the output to the outputText element
    const outputTextElement = document.getElementById('outputText');
    outputTextElement.textContent += event;
    outputTextElement.scrollTop = outputTextElement.scrollHeight; // Scroll to bottom
});





// HELPER FUNCTIONS

// Form validation - returns true / false (boolean)
/**
 * Validates the form data to ensure that the operation type, input path, and output path are selected.
 * 
 * @function validateForm
 * @returns {boolean} - Returns `true` if form data is valid, otherwise `false`.
 */
function validateForm() {
    // Log current data to console
    console.log("OperationType: ", operationType);
    console.log("Input: ", inPath);
    console.log("Output: ", outPath);

    if (!(operationType === undefined || inPath === undefined || outPath === undefined)) {
        if (!opArray.includes(operationType)) {
            return false;
        }
        return true;
    } else { 
        return false;
    }
}

// Pop-up alert message
/**
 * Displays an alert message on the UI using the Toastify library.
 * 
 * @function alertMessage
 * @param {string} message - The message to display.
 * @param {string} [bgColor="red"] - Background color of the message box.
 * @param {string} [txtColor="white"] - Text color of the message.
 */
function alertMessage(message, bgColor="red", txtColor="white") {
    toastify.toast({
        text: message,
        duration: 2000,
        close: false,
        style: {
            background: bgColor,
            color: txtColor,
            textAlign: 'center'
        }
    });
}

// Print Name
/**
 * Constructs a formatted print name for a directory path.
 * 
 * @function getPrintName
 * @param {string} dirPath - The directory path to construct the print name for.
 * @returns {string} - The formatted print name.
 */
function getPrintName(dirPath) {
    let basename = path.basename(dirPath);
    let absParentName = path.dirname(dirPath);
    let parentname = path.basename(path.dirname(dirPath));
    let grantName = path.basename(path.dirname(absParentName));
    let printName = path.join(`../`, grantName, parentname, basename);
    
    return printName
}

// Handle Input Path Selection
/**
 * Handles the selection of an input path, invoking the 'get-path' IPC function.
 * 
 * @function handleInPathSelection
 * @param {string} pathType - The type of path selection (e.g., 'openFile' or 'openDirectory').
 * @returns {Function} - Returns a function that handles the path selection.
 */
function handleInPathSelection(pathType) {
    return async () => {
        const result = await ipcRenderer.invoke('get-path', pathType);

        if (!result.canceled) {
            const selectedPath = result.path;
            inPath = selectedPath;
            const printName = getPrintName(inPath);
            dragDropBoxText.textContent = printName;
            console.log("Input Path:", inPath);
            assingInToOutPath(inPath);
        } else {
            if (inPath === undefined) {
                alertMessage("Please Select Valid Input Path", "red");
            }
        }
    };
}

// Assigns inPath to outPath
/**
 * Assigns the input path to the output path, updating the UI accordingly.
 * 
 * @function assignInToOutPath
 * @param {string} inPath - The selected input path.
 */
async function assingInToOutPath(inPath) {
    const filePath = inPath;
    const isFile = await fs.isFile(filePath);
    const isDir = await fs.isDir(filePath);
    
    if (isFile) {
        outPath = path.dirname(inPath)
        outPathButton.textContent = "Same as input. Click to change.";
        console.log("Output Path: ", outPath)
    } else if (isDir) {
        outPath = inPath
        outPathButton.textContent = "Same as input. Click to change.";
        console.log("Output Path: ", outPath)
    } else {
        alertMessage("Please select a valid input file/output path.", "red")
    }
}

/**
 * Disables various UI elements during an ongoing operation.
 * 
 * @function disableElements
 */
function disableElements() {
    // Input elements
    dragDropBox.classList.add("disabled");
    dragDropBoxText.classList.add("disabled");
    tooltip.classList.add("disabled");
    inFile.disabled = true;
    inFolder.disabled = true;
  
    // Output elements
    outPathButton.disabled = true;
  
    // Operation elements
    operationSelection.disabled = true;
  
    // Submit elements
    submitButton.disabled = true;
    
    // Disable form submission
    form.addEventListener('submit', (event) => {
      event.preventDefault();
    });
  }


/**
 * Enables UI elements after an operation finishes.
 * 
 * @function enableElements
 */
  function enableElements() {
    // Input elements
    dragDropBox.classList.remove("disabled");
    dragDropBoxText.classList.remove("disabled");
    tooltip.classList.remove("disabled");
    inFile.disabled = false;
    inFolder.disabled = false;
  
    // Output elements
    outPathButton.disabled = false;
  
    // Operation elements
    operationSelection.disabled = false;
  
    // Submit elements
    submitButton.disabled = false;
  
    // Re-enable form submission
    form.removeEventListener('submit', (event) => {
      event.preventDefault();
    });
  }


