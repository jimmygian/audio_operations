/**
 * main.js - Electron main script responsible for initializing the application.
 * This script sets up the main window, handles user interactions, and manages
 * communication with the backend and renderer processes (through preload.js).
 */

// Check that initial app works
console.log("main.js is working")


// MODULES
const { app, BrowserWindow, ipcMain, dialog, Menu } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');
// PATHS
const PYTHONSCRIPTPATH = path.join(__dirname, 'backend', 'audio_operations', 'audio_operations.py');
const PYTHONSCRIPTEXEC = path.join(__dirname, 'backend', 'executables', 'audio_operations.exe');
const INDEX = path.join(__dirname, 'renderer', 'index.html');
const PRELOADPATH = path.join(__dirname, 'preload.js');
// CONSTANTS
const AUDIOEXTENSIONS = ['wav', 'flac', 'ogg', 'aiff', 'aifc', 'mp3', 'aac'];
const isMac = process.platform === 'darwin'

// !!!! CHANGE THIS to "===" before packaging !!!!
const isDev = process.env.NODE_ENV === 'development'; 



// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}



// Create app's main window
/**
 * Creates the main Electron window and initializes its behavior.
 *
 * This function creates a new Electron BrowserWindow object, configures its properties,
 * and sets up event listeners to handle various actions.
 *
 * @function createMainWindow
 * @returns {void}
 */
function createMainWindow() {

  // MAKE NEW BROWSERWINDOW OBJECT

  // Create the browser window.
  const mainWindow = new BrowserWindow({
      // Basic configurations
      title: 'Basic Template',
      width: isDev ? 1000 : 580,
      height: 830,
      // Electron-specific configurations - must always be included
      webPreferences: {
          contextIsolation: true,
          nodeIntegration: true,
          preload: PRELOADPATH    // Path to where preload.js is
      }
  });

  // Open the DevTools if in Developer Mode
  if (isDev) {
      mainWindow.webContents.openDevTools();
  }

  // Handle "get-path" communication (when user needs to open window dialogue to select filees)
  ipcMain.handle('get-path', async (event, pathType) => {
      const result = await showFolderSelectionDialog(mainWindow, pathType);
      console.log(result)
      return result;
  });

  // Handle dropped files
  ipcMain.handle('files-dropped', async (event, filePaths) => {
      // Convert the file paths to absolute paths
      const absolutePaths = await filePaths.map((filePath) => path.resolve(filePath));
      return absolutePaths; // Array of abs paths
  });

  // Handle what happens on 'start-operation'
  ipcMain.on('start-operation', (event, data) => {
      const inputPath = path.normalize(data.inputPath);
      const outputPath = path.normalize(data.outputPath);
      const operation = data.operation;

      // Send message to renderer that operation has just started, just before calling Python
      event.sender.send('operation-started');

      // PYTHON - ELECTRON COMMUNICATION (using spawn from 'child_process')      
      let pythonProcess;
      if (isDev) {
          // Run python from system (python needs to be installed on system)
          pythonProcess = spawn('python', [PYTHONSCRIPTPATH, inputPath, outputPath, operation]);
      } else {
          // Run python from executable (python needs to be correctly compiled with pyinstaller for this to work)
          pythonProcess = spawn(PYTHONSCRIPTEXEC, [inputPath, outputPath, operation]);
      };
     
      
      // PYTHON OUTPUTS:

      // Declare variable that holds full message
      let messageFromPython = '';
      
      // Handle 'operation-finished' when Python process closes
      pythonProcess.on('close', (code) => {
          if (code === 0) {
              console.log(messageFromPython);
              
              // Send message to renderer.js that operation has finished. 'true' indicates successful python operation
              event.sender.send('operation-finished', "true");
          } else {
              const errorMessage = `Python process exited with code ${code}`;
              console.error(errorMessage);
              console.log(messageFromPython);
              
              // Send message to renderer.js that operation has finished. 'false' indicates python error
              event.sender.send('operation-finished', "false");
          }
      });
      
      // Send python's terminal output to renderer.js (front-end)
      pythonProcess.stdout.on('data', (data) => {
          const message = data.toString();
          messageFromPython += message;
          event.sender.send('python-output', message); // Send the output to renderer process
      });
      pythonProcess.stderr.on('data', (data) => {
          const errorMessage = `Python Error: ${data}`;
          console.error(errorMessage);
          event.sender.send('python-output', errorMessage); // Send the error output to renderer process
      });
  });

  // Set minimum window size
  mainWindow.setMinimumSize(500, 900);

  // And lastly, load the index.html of the app.
  mainWindow.loadFile(INDEX);
};

// ELECTRON PROCESS FOR CROSS-PLATFORM COMPATIBILITY


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createMainWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (!isMac) {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createMainWindow();
  }
});




// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.

// HELPER MAIN FUNCTIONS

/**
 * Show a folder selection dialog to the user.
 *
 * @param {BrowserWindow} window - The BrowserWindow object for dialog positioning.
 * @param {string} [path='openDirectory'] - The path type: 'openFile' or 'openDirectory'.
 * @returns {Promise<{selected: true, path: string}>} - Object indicating selected or canceled.
 */
async function showFolderSelectionDialog(window, path='openDirectory') {
  const properties = path === 'openFile' ? ['openFile'] : ['openDirectory'];
  const accept = path === 'openFile' ? AUDIOEXTENSIONS : null;

  const userPath = await dialog.showOpenDialog(window, {
      properties: properties,
      filters: [{ name: 'Audio Files', extensions: accept }]
  });

  if (!userPath.canceled) {
      const selectedPath = userPath.filePaths[0];
      console.log("Selected path:", selectedPath);
      return { selected: true, path: selectedPath };
  } else {
      console.log("Path selection cancelled.");
      return { canceled: true };
  }
}
