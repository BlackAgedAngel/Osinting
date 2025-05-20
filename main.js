const { app, BrowserWindow } = require('electron');
const path = require('path');
const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const PORT = 5000;

const serverApp = express();
serverApp.use(cors());
serverApp.use(express.json());

serverApp.post('/summarize', (req, res) => {
    const osintData = req.body;
    const py = spawn('python', ['osint_profile.py']);
    let output = '';
    py.stdin.write(JSON.stringify(osintData));
    py.stdin.end();
    py.stdout.on('data', (data) => { output += data.toString(); });
    py.stdout.on('end', () => { res.send(output); });
    py.stderr.on('data', (data) => { console.error(data.toString()); });
});

serverApp.post('/osint-links', (req, res) => {
    const osintData = req.body;
    const py = spawn('python', ['osint_profile.py', 'links']);
    let output = '';
    py.stdin.write(JSON.stringify(osintData));
    py.stdin.end();
    py.stdout.on('data', (data) => { output += data.toString(); });
    py.stdout.on('end', () => {
        try {
            res.json(JSON.parse(output));
        } catch (e) {
            res.status(500).send('Error parsing links');
        }
    });
    py.stderr.on('data', (data) => { console.error(data.toString()); });
});

serverApp.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
