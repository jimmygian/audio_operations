// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts


/**
 * preload.js - This script serves as a bridge between the main (main.js) Electron process and the renderer (renderer.js) process.
 * It exposes selected modules, functions, and objects to the renderer process for secure communication.
 *
 * @module MainBridge
 */

// Import necessary modules that you need to expose to renderer.js
const os = require('os');
const path = require('path');
const Toastify = require('toastify-js');
const fs = require('fs');
const { contextBridge, ipcRenderer } = require('electron');


// EXPOSES:

// Expose 'os' module functions to the renderer process
contextBridge.exposeInMainWorld('os', {
    homedir: () => os.homedir()
});

// Expose 'path' module functions and add 'cwd' property to the renderer process
contextBridge.exposeInMainWorld('path', {
    join: (...args) => path.join(...args),
    relative: (abPath, target) => path.relative(abPath, target),
    basename: (abPath) => path.basename(abPath),
    dirname: (abPath) => path.dirname(abPath),
    normalize: (abPath) => path.normalize(abPath),
    cwd: process.cwd() // Expose current working directory
});

// Expose 'ipcRenderer' object with 'invoke' method to the renderer process
// This returns the absolute path of a folder the user selects in an <input> tag
contextBridge.exposeInMainWorld('ipcRenderer', {
    invoke: (...args) => ipcRenderer.invoke(...args),
    send: (channel, data) => ipcRenderer.send(channel, data),
    on: (channel, func) => 
        ipcRenderer.on(channel, (event, ...args) => func(...args))
});

// Expose 'os' module functions to the renderer process
contextBridge.exposeInMainWorld('toastify', {
    toast: (options) => Toastify(options).showToast(),
});

// Expose custom functions in the fs object
contextBridge.exposeInMainWorld('fs', {
    isFile: async (filePath) => {
        try {
            const stats = await fs.promises.stat(filePath);
            return stats.isFile();
        } catch (error) {
            console.error(error);
            return false;
        }
    },
    isDir: async (dirPath) => {
        try {
            const stats = await fs.promises.stat(dirPath);
            return stats.isDirectory();
        } catch (error) {
            console.error(error);
            return false;
        }
    }
});


/**
 * The Electron `contextBridge` is a security feature that enables safe communication between the main process
 * and the renderer process by exposing selected modules, functions, and objects to the renderer process.
 * This allows controlled access to APIs while preventing direct access to potentially sensitive or unsafe operations.
 * 
 * @namespace contextBridge
 * @see {@link https://www.electronjs.org/docs/api/context-bridge|Electron Context Bridge Documentation}
 * @see {@link https://www.electronjs.org/docs/tutorial/security#3-enable-context-isolation-for-remote-content|Electron Security Documentation}
 */