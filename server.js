// constants for server to start the web interface and handle serial communication with Nicla Vision
const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.json());
const EMPLOYER_USER = 'admin';
const EMPLOYER_PASS = 'password123';
const portName = 'COM5'; 
const baudRate = 9600;
app.use(express.static('public'));

// Serial Port Communication (Very important) 
let serialPort;
try {
  serialPort = new SerialPort({ path: portName, baudRate: baudRate });
} catch (error) {
  console.error(`Error: Could not open serial port ${portName}.`, error.message);
  process.exit(1);
}
const parser = serialPort.pipe(new ReadlineParser({ delimiter: '\n' }));

serialPort.on('error', (err) => {
    console.error('SerialPort Error: ', err.message);
});
// Getting data from the push buttons on what gear to check for
parser.on('data', (data) => {
  console.log('Data from Nicla:', data);
  if (data.startsWith('GEAR_LIST:')) {
    const listString = data.substring(10).trim();
    io.emit('gear-list-update', listString);
  }
});
// Detecting results from Nicla Vision
parser.on('data', (data) => {
  console.log('Data from Nicla Vision:', data);
  if (data.startsWith('RESULT:')) {
    const userMessage = data.substring(7); 
    io.emit('detection', userMessage); 
  } else if (data.startsWith('ERROR:')) {
    io.emit('detection', data);
  }
});

// Socket.IO Communication for users to interact with the web page
io.on('connection', (socket) => {
  console.log('A user connected to the web page.');
  socket.on('start-check', (data) => {
    if (data && data.username) {
      console.log(`Received 'start-check' for user: ${data.username}`);
      const command = `START_CHECK:${data.username}\n`;
      serialPort.write(command, (err) => {
        if (err) return console.log('Error on write: ', err.message);
        console.log('Start command sent to Nicla Vision.');
      });
    }
  });
  socket.on('disconnect', () => {
    console.log('User disconnected from the web page.');
  });
});

// Routes for serving HTML files
app.get('/', (req, res) => { res.sendFile(__dirname + '/public/login.html'); });
app.get('/dashboard', (req, res) => { res.sendFile(__dirname + '/public/dashboard.html'); });
app.get('/employer-settings', (req, res) => { res.sendFile(__dirname + '/public/employer-settings.html'); });
app.get('/employer-login', (req, res) => {
  res.sendFile(__dirname + '/public/employer-login.html');
});

app.post('/login-employer', (req, res) => {
  const { username } = req.body;
  
  console.log(`Employer '${username}' has accessed the settings page.`);
  res.status(200).json({ status: 'logged' });
});

// web interface link
const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server is live at http://localhost:${PORT}`);
  console.log(`Attempting to listen to Nicla Vision on port ${portName}...`);
});