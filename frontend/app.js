/* Copyright MENTAL Front End Team 2018 */
/* All Rights Reserved */
/* Made with love <3 */

'use strict';
require('dotenv').config()
/* SET UP SERVER */
const express = require('express'); // Creates the server
const app     = express();
const server  = require('http').createServer(app); // Ensures it's HTTP
const path    = require('path'); // Directory/path handling
const io      = require('socket.io')(server); // Sets up a socket
const osc     = require('osc.io');
const mail    = require('nodemailer');


const transporter = mail.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL,
    pass: process.env.PASSWORD
  }
});

let mailOptions = {
  from: 'mcgillneurotech@gmail.com',
  to: 'nyk.mirchi@gmail.com',
  subject: 'Sent from MENTAL P300 user',
  text: 'Ping from P300 machine'
};

io.set('browser client minification', true);
io.set('browser client etag', true);
io.set('browser client gzip', true);
io.set('browser client expires', true);


/* DIRECTORIES */
app.set('port', process.env.PORT || 3000);
app.use(express.static(path.join(__dirname, 'public'))); //Put public files (JS, CSS, images) in here

/* SOCKET */

var connections = []

io.on('connection', (socket) => {
	console.log("new connection on socket");

  // Front end will send a start message, and
  // This will begin
  let testMsg = ['h', 'e', 'y', '🍕'];
// let testMsg = ['👋'];
  let index = 0;

  setInterval(function() {
    socket.emit('message', testMsg[index]);
    index++;
//}, 17700);
  }, 2500);

  socket.on('sendmail', function(msg) {

    console.log('here we are');
    mailOptions.to = msg;

    transporter.sendMail(mailOptions, function(error, info){
      if (error) {
        console.log(error);
      } else {
        console.log('Email sent: ' + info.response);
      }
    });
  })


	
  socket.once('disconnect', () => {
      connections.splice(connections.indexOf(socket), 1);
      socket.disconnect();
      console.log('Disconnected: %s. Remained: %s.', socket.id, connections.length)
  });

  connections.push(socket);
})

/* START SERVER */
server.listen(app.get('port'), () => {
	console.log('Listening on port 3000...')
});
