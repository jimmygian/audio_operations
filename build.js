const packager = require('electron-packager');
const path = require('path');

// Options for packaging the Electron app
const options = {
  dir: __dirname, // Path to your Electron app directory
  out: path.join(__dirname, 'out'), // Output directory for the packaged app
  platform: 'win32', // e.g., 'win32', 'darwin', 'linux'
  arch: 'x64', // e.g., 'x64', 'ia32', 'arm64'
  electronVersion: '26.1.0', // e.g., '15.2.0'
  overwrite: true, // Overwrite output directory if it already exists
};

// Package the Electron app
packager(options)
  .then(appPaths => {
    console.log('App packaged successfully:', appPaths);
  })
  .catch(err => {
    console.error('Error packaging app:', err);
  });


