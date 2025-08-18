const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let backendProcess = null;

function createWindow() {
  const win = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  win.loadFile('login.html'); // Cambia esto si tu página principal es otra
}

app.whenReady().then(() => {
  // Inicia el backend Python
  backendProcess = spawn('python', [path.join(__dirname, '../backend/app.py')], {
    cwd: path.join(__dirname, '../backend'),
    shell: true,
    detached: true,
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });
  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend error: ${data}`);
  });

  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    if (backendProcess) backendProcess.kill();
    app.quit();
  }
});
