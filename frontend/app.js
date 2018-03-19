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

const dgram = require('dgram');
const udp = dgram.createSocket('udp4');

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

  /* START UDP SERVER */
  udp.on('error', (err) => {
    console.log(`udp server error:\n${err.stack}`);
    server.close();
  });

  udp.on('message', (msg, rinfo) => {
    console.log(`udp server got message: ${msg.toString()} from ${rinfo.address}:${rinfo.port}`);
    let location = msg.toString().split(',')[0];
    socket.emit('message', location);
  });

  udp.on('listening', () => {
    const address = server.address();
    console.log(`udp server listening ${address.address}:${address.port}`);
  });


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
