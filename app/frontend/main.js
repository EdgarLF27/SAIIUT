const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let flaskProcess;

function createWindow() {
  const win = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      contextIsolation: true
    }
    // Puedes agregar icon: path.join(__dirname, 'ruta/a/tu/icono.ico') si tienes un icono
  });

  win.loadFile('login.html');
}

app.whenReady().then(() => {
  flaskProcess = spawn(
  'python',
  [path.join(__dirname, '../backend/app.py')],
  {
    cwd: path.join(__dirname, '../backend')
  }
);


  flaskProcess.stdout.on('data', (data) => {
    console.log(`Flask: ${data}`);
  });

  flaskProcess.stderr.on('data', (data) => {
    console.error(`Flask error: ${data}`);
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (flaskProcess) flaskProcess.kill();
  if (process.platform !== 'darwin') app.quit();
});
